from rest_framework import serializers
from .models import Coupon, Promotion
from restaurants.serializers import SimpleRestaurantSerializer

class CouponSerializer(serializers.ModelSerializer):
    restaurant = SimpleRestaurantSerializer(read_only=True)
    discount = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        exclude = ['id'] 

    def get_discount(self, obj):
        if not obj.discount_type or obj.discount_value is None:
            return None

        if obj.discount_type == "金額":
            return f"{obj.discount_value}元 折價券"
        elif obj.discount_type == "百分比":            
            discount_rate = round(10 - obj.discount_value / 10, 1)
            return f"{discount_rate}折 折價券"
        else:
            return "未知折扣類型"
        
class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        exclude = ['id']