from django.shortcuts import render
from rest_framework import viewsets
from .models import Coupon
from .serializers import CouponSerializer

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.filter(is_archived=False)
    serializer_class = CouponSerializer
    lookup_field = 'uuid'
