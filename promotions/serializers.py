from rest_framework import serializers
from .models import Coupon
from restaurants.models import Restaurant

class RestaurantSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name','image_url']

class CouponSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSimpleSerializer(read_only=True)

    class Meta:
        model = Coupon
        exclude = ['id'] 