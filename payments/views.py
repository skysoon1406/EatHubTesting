from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from payments.models import PaymentOrder, Subscription, Product
from users.utils import optional_token_cbv
from users.models import User
import uuid
import requests
from django.conf import settings

# Create your views here.
class SubscriptionCreateView(APIView):
    @optional_token_cbv
    def post(self, request):
        user_uuid = request.user_uuid
        try:
            user = User.objects.get(uuid=user_uuid)
        except User.DoesNotExist:
            return Response({'error':'找不倒使用者'}, status=status.HTTP_404_NOT_FOUND)
        
        product_id = request.data.get('product_id')
        amount_input = request.data.get('amount')
        
        if not product_id or not amount_input:
            return Response({'error':'缺少參數'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            amount = int(amount_input)
        except ValueError:
            return Response({'error': '金額需是數字'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product = Product.objects.get(uuid=product_id)
        except Product.DoesNotExist:
            return Response({'error':'找不到對應產品'}, status=status.HTTP_404_NOT_FOUND)
        
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

        headers={
            'Content-Type': 'application/json',
            'X-LINE-ChannelId': settings.LINEPAY_CHANNEL_ID,
            'X-LINE-ChannelSecret': settings.LINEPAY_CHANNEL_SECRET,
        }
        print("📦 Content-Type:", headers.get('Content-Type'))
        print("📦 X-LINE-ChannelId:", headers.get('X-LINE-ChannelId'))
        print("📦 X-LINE-ChannelSecret:", headers.get('X-LINE-ChannelSecret'))
        body ={
            'amount': amount,
            'currency': 'TWD',
            'orderId': order_id,
            'packages': [
                {
                    'id': str(uuid.uuid4()),
                    'amount': amount,
                    'name':product.name,
                    'products': [
                        {
                            'name':product.name,
                            'quantity':1,
                            'price':amount
                        }
                    ]
                }
            ],
            'redirectUrls':{
                "confirmUrl": "https://localhost:8000/api/payments/confirm",
                "cancelUrl": "https://localhost:8000/payment-cancel",
            }
        }
        try:
            res = requests.post(
                "https://sandbox-api-pay.line.me/v3/payments/request",
                headers=headers,
                json=body
            )
            data = res.json()
        except requests.exceptions.RequestException as e:
            return Response({'error': '連線 LINE PAY 失敗', 'details': str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        
        if data.get('returnCode') == '0000':
            return Response({
                'order_id': order_id,
                'payment_url_web': data['info']['paymentUrl']['web'],
                'payment_url_app': data['info']['paymentUrl']['app']
            })
        else:
            return Response({'error': data.get('returnMessage')}, status=status.HTTP_400_BAD_REQUEST)