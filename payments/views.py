import uuid
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from payments.models import PaymentOrder, Product
from users.models import User
from users.utils import token_required_cbv, check_merchant_role
from .subscription_service import create_subscription_after_payment
from .payment_flow import prepare_payment_order
from .linepay_service import LinePayService
from payments.serializers import ProductSerializer,PaymentOrderSerializer

class ProductListView(APIView):
    @token_required_cbv
    @check_merchant_role
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

# 建立付款訂單與 LINE PAY 請求
class SubscriptionCreateView(APIView):
    @token_required_cbv
    @check_merchant_role
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

        try:
            payment_order, *_ = prepare_payment_order(user, product, amount)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        service = LinePayService(payment_order, product)
        try:
            data = service.send_payment_request()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        if amount != product.amount:
            return Response({'error': '金額不正確'}, status=status.HTTP_400_BAD_REQUEST)

        if data.get('returnCode') == '0000':
            return Response({
                'order_id': payment_order.order_id,
                'payment_url_web': data['info']['paymentUrl']['web'],
                'payment_url_app': data['info']['paymentUrl']['app']
            })
        else:
            return Response({'error': data.get('returnMessage')}, status=status.HTTP_400_BAD_REQUEST)


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
        
        service = LinePayService(payment_order, payment_order.product)
        try:
            data = service.confirm_payment(transaction_id)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        if data.get('returnCode') == '0000':
            subscription = create_subscription_after_payment(payment_order.user, payment_order.product)
            payment_order.subscription = subscription
            payment_order.is_paid = True
            payment_order.transaction_id = transaction_id
            payment_order.save()
            return Response({'message': '付款確認成功', 'transactionId': transaction_id})
        else:
            return Response({'error': data.get('returnMessage')}, status=status.HTTP_400_BAD_REQUEST)

class PaymentOrderDetailView(APIView):
    def get(self, request, order_id):
        try:
            payment_order = PaymentOrder.objects.get(order_id=order_id)
        except PaymentOrder.DoesNotExist:
            return Response({'error': '找不到訂單'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PaymentOrderSerializer(payment_order)
        return Response({'result': serializer.data}, status=status.HTTP_200_OK)