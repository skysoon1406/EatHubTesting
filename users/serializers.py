from rest_framework import serializers
from .models import User, UserCoupon
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




class MerchantSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'user_name', 'license_url']

    def validate_password(self, value):
        return make_password(value)

    def create(self, validated_data):
        # 強制指定角色為商家
        validated_data['role'] = User.Role.MERCHANT
        return User.objects.create(**validated_data)