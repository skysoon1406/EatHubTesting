import uuid
import json
import requests
import hmac
import hashlib
import base64
from django.conf import settings
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from payments.models import PaymentOrder, Subscription, Product, PaymentLog
from users.models import User
from users.utils import optional_token_cbv

# 建立付款訂單與 LINE PAY 請求
class SubscriptionCreateView(APIView):
    @optional_token_cbv
    def post(self, request):
        user_uuid = request.user_uuid
        try:
            user = User.objects.get(uuid=user_uuid)
        except User.DoesNotExist:
            return Response({'error': '找不到使用者'}, status=status.HTTP_404_NOT_FOUND)

        product_id = request.data.get('product_id')
        amount_input = request.data.get('amount')

        if not product_id or not amount_input:
            return Response({'error': '缺少參數'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            amount = int(amount_input)
        except ValueError:
            return Response({'error': '金額需是數字'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(uuid=product_id)
        except Product.DoesNotExist:
            return Response({'error': '找不到產品'}, status=status.HTTP_404_NOT_FOUND)

        # 建立訂閱與訂單資料
        today = timezone.now().date()
        next_date = today + timezone.timedelta(days=product.interval_days)
        subscription = Subscription.objects.create(user=user, product=product, next_payment_date=next_date)

        order_id = f'order_{today.strftime("%Y%m%d")}_{uuid.uuid4().hex[:8]}'
        payment_order = PaymentOrder.objects.create(
            order_id=order_id,
            user=user,
            subscription=subscription,
            amount=amount,
            product=product
        )

        # 組裝 LINE PAY 請求資料
        body = {
            "amount": amount,
            "currency": "TWD",
            "orderId": order_id,
            "packages": [
                {
                    "id": str(uuid.uuid4()),
                    "amount": amount,
                    "name": product.name,
                    "products": [
                        {
                            "name": product.name,
                            "quantity": 1,
                            "price": amount
                        }
                    ]
                }
            ],
            "redirectUrls": {
                "confirmUrl": f"{settings.PUBLIC_DOMAIN}/api/v1/payments/confirm",
                "cancelUrl": f"{settings.PUBLIC_DOMAIN}/payment-cancel"
            }
        }

        # 產生簽章
        api_path = "/v3/payments/request"
        nonce = uuid.uuid4().hex
        body_str = json.dumps(body)
        message = settings.LINEPAY_CHANNEL_SECRET + api_path + body_str + nonce
        signature = base64.b64encode(
            hmac.new(settings.LINEPAY_CHANNEL_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).digest()
        ).decode('utf-8')
        headers = {
            "Content-Type": "application/json",
            "X-LINE-ChannelId": settings.LINEPAY_CHANNEL_ID,
            "X-LINE-Authorization-Nonce": nonce,
            "X-LINE-Authorization": signature,
        }

        # 發送付款請求
        try:
            res = requests.post(f"{settings.LINEPAY_API_BASE_URL}{api_path}", headers=headers, json=body)
            data = res.json()
        except Exception as e:
            PaymentLog.objects.create(
                payment_order=payment_order,
                request_payload=body,
                response_payload={"error": str(e)},
                return_code='EXCEPTION',
                return_message='Request failed'
            )
            return Response({'error': str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        PaymentLog.objects.create(
            payment_order=payment_order,
            request_payload=body,
            response_payload=data,
            return_code=data.get('returnCode', 'N/A'),
            return_message=data.get('returnMessage', 'N/A')
        )
        if data.get("returnCode") == "0000":
            return Response({
                "order_id": order_id,
                "payment_url_web": data['info']['paymentUrl']['web'],
                "payment_url_app": data['info']['paymentUrl']['app']
            })
        else:
            return Response({"error": data.get("returnMessage")}, status=status.HTTP_400_BAD_REQUEST)


# 使用者付款成功後，LINE PAY 會自動導向 confirmUrl（GET 請求）
class LinePayConfirmView(APIView):
    def get(self, request):
        return self.handle_confirmation(request)

    def post(self, request):
        return self.handle_confirmation(request)

    def handle_confirmation(self, request):
        transaction_id = request.query_params.get('transactionId') or request.data.get('transactionId')
        order_id = request.query_params.get('orderId') or request.data.get('orderId')

        if not transaction_id or not order_id:
            return Response({'error': '缺少必要參數'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment_order = PaymentOrder.objects.get(order_id=order_id)
        except PaymentOrder.DoesNotExist:
            return Response({'error': '找不到訂單'}, status=status.HTTP_404_NOT_FOUND)

        # LINE PAY 付款確認
        body = {
            "amount": payment_order.amount,
            "currency": "TWD"
        }

        api_path = f"/v3/payments/{transaction_id}/confirm"
        nonce = uuid.uuid4().hex
        body_str = json.dumps(body)
        message = settings.LINEPAY_CHANNEL_SECRET + api_path + body_str + nonce
        signature = base64.b64encode(
            hmac.new(settings.LINEPAY_CHANNEL_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).digest()
        ).decode('utf-8')
        headers = {
            "Content-Type": "application/json",
            "X-LINE-ChannelId": settings.LINEPAY_CHANNEL_ID,
            "X-LINE-Authorization-Nonce": nonce,
            "X-LINE-Authorization": signature,
        }

        try:
            url = f"{settings.LINEPAY_API_BASE_URL}{api_path}"
            res = requests.post(url, headers=headers, json=body)
            data = res.json()
        except Exception as e:
            PaymentLog.objects.create(
                payment_order=payment_order,
                request_payload=body,
                response_payload={"error": str(e)},
                return_code='EXCEPTION',
                return_message='Request failed'
            )
            return Response({'error': str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        PaymentLog.objects.create(
            payment_order=payment_order,
            request_payload=body,
            response_payload=data,
            return_code=data.get('returnCode', 'N/A'),
            return_message=data.get('returnMessage', 'N/A')
        )
        
        if data.get('returnCode') == '0000':
            payment_order.is_paid = True
            payment_order.transaction_id = transaction_id
            payment_order.save()
            return Response({'message': '付款確認成功', 'transactionId': transaction_id})
        else:
            return Response({'error': data.get('returnMessage')}, status=status.HTTP_400_BAD_REQUEST)
