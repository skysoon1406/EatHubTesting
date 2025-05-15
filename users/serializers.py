from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password


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
