from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from payments.models import PaymentOrder, Subscription, Product
from users.utils import optional_token_cbv
from users.models import User
from django.conf import settings
import uuid, requests, json, hmac, hashlib, base64, time, json

#付款請求
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
            return Response({'error': '找不到對應產品'}, status=status.HTTP_404_NOT_FOUND)

        today = timezone.now().date()
        next_date = today + timezone.timedelta(days=product.interval_days)

        subscription = Subscription.objects.create(
            user=user,
            product=product,
            next_payment_date=next_date,
        )

        today_str = today.strftime('%Y%m%d')
        order_id = f'order_{today_str}_{uuid.uuid4().hex[:8]}'

        paymentorder = PaymentOrder.objects.create(
            order_id=order_id,
            user=user,
            subscription=subscription,
            amount=amount,
            product=product
        )

        # LINE PAY body
        body = {
            'amount': amount,
            'currency': 'TWD',
            'orderId': order_id,
            'packages': [
                {
                    'id': str(uuid.uuid4()),
                    'amount': amount,
                    'name': product.name,
                    'products': [
                        {
                            'name': product.name,
                            'quantity': 1,
                            'price': amount
                        }
                    ]
                }
            ],
            "redirectUrls": {
                "confirmUrl": "https://sandbox-api-pay.line.me/orders/confirm",
                "cancelUrl":  "https://sandbox-api-pay.line.me/orders/cancel"
            }
        }
        # HMAC 簽章計算
        api_path = "/v3/payments/request"
        nonce = uuid.uuid4().hex
        body_str = json.dumps(body)
        message = settings.LINEPAY_CHANNEL_SECRET + api_path + body_str + nonce
        signature = base64.b64encode(
            hmac.new(
                settings.LINEPAY_CHANNEL_SECRET.encode('utf-8'),
                message.encode('utf-8'),
                hashlib.sha256
            ).digest()
        ).decode('utf-8')
        
        # 設定 header
        headers = {
            "Content-Type": "application/json",
            "X-LINE-ChannelId": settings.LINEPAY_CHANNEL_ID,
            "X-LINE-Authorization-Nonce": nonce,
            "X-LINE-Authorization": signature,
        }

        try:
            res = requests.post(
                f"{settings.LINEPAY_API_BASE_URL}/v3/payments/request",
                headers=headers,
                json=body
            )
            data = res.json()
        except requests.exceptions.RequestException as e:
            return Response({'error': '連線 LINE PAY 失敗', 'details': str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        if data.get('returnCode') == '0000':
            pay_status = data["info"].get("payStatus")
            transaction_id = data["info"].get("transactionId")

            if pay_status == 'PAYMENT_SUCCESS':
                PaymentOrder.objects.filter(
                    order_id=order_id,
                    is_paid=False
                ).update(
                    is_paid=True,
                    transaction_id=transaction_id
                )
            
            return Response({
                'order_id': order_id,
                'transaction_id': data['info']['transactionId'],
                'payment_url_web': data['info']['paymentUrl']['web'],
                'payment_url_app': data['info']['paymentUrl']['app']
            })
        else:
            return Response({'error': data.get('returnMessage')}, status=status.HTTP_400_BAD_REQUEST)

class LinePayConfirmView(APIView):
    def get(self, request):
        transaction_id = request.query_params.get('transactionId')
        order_id = request.query_params.get('orderId')

        if not transaction_id or not order_id:
            return Response({'error': '缺少必要參數'}, status=status.HTTP_400_BAD_REQUEST)

        api_path = f"/v3/payments/{transaction_id}/confirm"
        nonce = uuid.uuid4().hex

        body = {
            "amount": 10690,
            "currency": "TWD"
        }

        message = settings.LINEPAY_CHANNEL_SECRET + api_path + json.dumps(body, separators=(',', ':')) + nonce
        signature = base64.b64encode(hmac.new(
            settings.LINEPAY_CHANNEL_SECRET.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).digest()).decode()

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
            return Response({'error': str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        if data.get('returnCode') == '0000':
            # 更新你本地的付款狀態
            try:
                payment_order = PaymentOrder.objects.get(order_id=order_id)
                payment_order.is_paid = True
                payment_order.save()
            except PaymentOrder.DoesNotExist:
                return Response({'error': '找不到訂單'}, status=status.HTTP_404_NOT_FOUND)

            return Response({'message': '付款成功', 'transactionId': transaction_id})
        else:
            return Response({'error': data.get('returnMessage')}, status=status.HTTP_400_BAD_REQUEST)


class LinePayOrderStatusView(APIView):
    def get(self, request, order_id):
        try:
            payment_order = PaymentOrder.objects.get(order_id=order_id)
        except PaymentOrder.DoesNotExist:
            return Response({'error': '訂單不存在'}, status=status.HTTP_404_NOT_FOUND)

        # LINE Pay 查詢付款狀態
        api_path = f"/v3/payments/orders/{order_id}/check"
        nonce = uuid.uuid4().hex
        message = settings.LINEPAY_CHANNEL_SECRET + api_path + nonce

        signature = base64.b64encode(
            hmac.new(
                settings.LINEPAY_CHANNEL_SECRET.encode('utf-8'),
                message.encode('utf-8'),
                hashlib.sha256
            ).digest()
        ).decode('utf-8')

        headers = {
            "Content-Type": "application/json",
            "X-LINE-ChannelId": settings.LINEPAY_CHANNEL_ID,
            "X-LINE-Authorization-Nonce": nonce,
            "X-LINE-Authorization": signature,
        }

        url = f"{settings.LINEPAY_API_BASE_URL}{api_path}"

        try:
            res = requests.get(url, headers=headers)
            data = res.json()
            print("📦 LINE PAY 查詢回傳：", data)
        except Exception as e:
            return Response({'error': f'LINE PAY 查詢失敗: {str(e)}'}, status=status.HTTP_502_BAD_GATEWAY)

        if data.get("returnCode") == "0000":
            pay_status = data["info"].get("payStatus")

            # 更新付款狀態
            if pay_status == "PAYMENT_SUCCESS" and not payment_order.is_paid:
                payment_order.is_paid = True
                payment_order.save()

            return Response({
                "orderId": payment_order.order_id,
                "amount": payment_order.amount,
                "isPaid": payment_order.is_paid,
                "linePayStatus": pay_status,
                "linePayTransactionId": data["info"].get("transactionId")
            })

        else:
            return Response({'error': data.get("returnMessage")}, status=status.HTTP_400_BAD_REQUEST)