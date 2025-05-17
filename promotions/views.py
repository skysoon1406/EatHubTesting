from rest_framework import viewsets, status
from .models import Coupon
from .serializers import CouponSerializer
from rest_framework.views import APIView
from users.utils import token_required_cbv  
from django.shortcuts import get_object_or_404
from users.models import User, UserCoupon
from rest_framework.response import Response

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
