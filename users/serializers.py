from rest_framework import serializers
from .models import User, UserCoupon, Favorite
from django.contrib.auth.hashers import make_password
from promotions.serializers import CouponSerializer

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'user_name', 'email', 'password']

    def validate_password(self, value):
        return make_password(value)

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserCouponListSerializer(serializers.ModelSerializer):
    coupon = CouponSerializer(read_only=True) 

    class Meta:
        model = UserCoupon
        fields = [
            'uuid',
            'is_used',
            'claimed_at',
            'used_at',
            'coupon',  
        ]
class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_name', 'image_url', 'uuid']

class FavoriteSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        from restaurants.serializers import RestaurantSerializer 
        self._declared_fields['restaurant'] = RestaurantSerializer(read_only=True)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Favorite
        fields = ['restaurant', 'created_at']