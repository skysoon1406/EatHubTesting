from django.shortcuts import render
from rest_framework import viewsets
from .models import Coupon
from .serializers import CouponSerializer

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