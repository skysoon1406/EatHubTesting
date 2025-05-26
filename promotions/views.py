from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from users.utils import token_required_cbv
from users.models import User, UserCoupon
from .models import Coupon, Promotion
from .serializers import CouponSerializer, PromotionsCreateSerializer
from django.utils.decorators import method_decorator

"""
GET /api/v1/coupons/<uuid>/
result = {
    "restaurant": {
        "name": "五倍咖啡",
        "imgUrl": "https://example.com/restaurant.jpg"
    },
    "serialNumber": "test20240510",
    "endedAt": "2025-05-10T05:08:40Z",
    "createdAt": "2025-05-10T05:09:41.174907Z",
    "title": "test01",
    "description": "滿500折50",
    "discountType": "amount",
    "discountValue": 50,
    "total": 100,
    "isArchived": false,
    "startedAt": "2025-05-10T05:09:39Z",
    "uuid": "cd37115d-ce26-42e1-a71b-ceb66d54e163"
}

POST /api/v1/coupons/
body = {
  "serialNumber": "test20240510",
  "title": "test01",
  "description": "滿500折50",
  "discountType": "amount",
  "discountValue": 50,
  "total": 100,
  "startedAt": "2025-05-10T05:09:39Z",
  "endedAt": "2025-05-10T05:08:40Z",
  "isArchived": false
}
#  201 Created
result = {
  "serialNumber": "test20240510",
  "title": "test01",
  "description": "滿500折50",
  "discountType": "amount",
  "discountValue": 50,
  "total": 100,
  "isArchived": false,
  "startedAt": "2025-05-10T05:09:39Z",
  "endedAt": "2025-05-10T05:08:40Z",
  "createdAt": "2025-05-13T07:15:41.120000Z",
  "uuid": "cd37115d-ce26-42e1-a71b-ceb66d54e163",
  "restaurant": {
    "name": "五倍咖啡",
    "imgUrl": "https://example.com/restaurant.jpg"
  }
}
#  400 Bad Request 
result = {
  "serialNumber": ["此欄位為必填"],
  "discountType": ["此欄位為必填"],
  "discountValue": ["此欄位為必填"]
}
"""
class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.filter(is_archived=False)
    serializer_class = CouponSerializer
    lookup_field = 'uuid'  # 使用 uuid 作為查詢欄位

    #自動把目前登入的使用者的 restaurant 塞進去
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(restaurant=user.restaurant)

class ClaimCouponView(APIView):
    @token_required_cbv
    def post(self, request, uuid):
        user = get_object_or_404(User, uuid=request.user_uuid)
        coupon = get_object_or_404(Coupon, uuid=uuid, is_archived=False)

        if UserCoupon.objects.filter(user=user, coupon=coupon).exists():
            return Response({'success': False}, status=status.HTTP_200_OK)
        
        UserCoupon.objects.create(user=user, coupon=coupon)
        return Response({'success': True}, status=status.HTTP_201_CREATED)
    
class PromotionCreateView(APIView):
    @token_required_cbv
    def post(self, request):
        user = get_object_or_404(User, uuid=request.user_uuid)

        if user.role not in ['merchant', 'vip_merchant']:
            return Response({'error': '此帳戶無建立動態權限'}, status=status.HTTP_403_FORBIDDEN)

        if not user.restaurant:
            return Response({'error': '帳戶未綁定餐廳'}, status=status.HTTP_403_FORBIDDEN)

        promotion_count = user.restaurant.promotions.filter(is_archived=False).count()
        limit = 3 if user.role == 'vip_merchant' or user.is_vip else 1

        if promotion_count >= limit:
            role_display = 'VIP 商家' if user.is_vip else '一般商家'
            return Response({'error': f'{role_display} 最多只能建立 {limit} 則動態'}, status=400)

        serializer = PromotionsCreateSerializer(data=request.data, context={
            'request': request,
            'restaurant': user.restaurant,
        })
        if serializer.is_valid():
            promotion = serializer.save()
            return Response(PromotionsCreateSerializer(promotion).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)