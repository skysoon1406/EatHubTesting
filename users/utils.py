from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
from functools import wraps
from django.shortcuts import get_object_or_404
from users.models import User
from django.utils import timezone

# CBV驗證裝飾器
def token_required_cbv(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        raw_token = request.COOKIES.get('auth_token')
        if not raw_token or ':' not in raw_token:
            return Response(
                {'error': '未提供 Token'}, status=status.HTTP_401_UNAUTHORIZED
            )
        user_uuid, token = raw_token.split(':', 1)

        cache_key = f'user_token:{user_uuid}'
        stored_token = cache.get(cache_key)

        if stored_token != token:
            return Response(
                {'error': 'Token 驗證失敗'}, status=status.HTTP_401_UNAUTHORIZED
            )
        request.user_uuid = user_uuid
        return view_func(self, request, *args, **kwargs)

    return wrapper

# FBV驗證裝飾器
def token_required_fbv(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        raw_token = request.COOKIES.get('auth_token')
        if not raw_token or ':' not in raw_token:
            return Response(
                {'error': '未提供 Token'}, status=status.HTTP_401_UNAUTHORIZED
            )
        user_uuid, token = raw_token.split(':', 1)

        cache_key = f'user_token:{user_uuid}'
        stored_token = cache.get(cache_key)

        if stored_token != token:
            return Response(
                {'error': 'Token 驗證失敗'}, status=status.HTTP_401_UNAUTHORIZED
            )
        request.user_uuid = user_uuid
        return view_func(request, *args, **kwargs)

    return wrapper

def optional_token_cbv(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        raw_token = request.COOKIES.get('auth_token')
        request.user_uuid = None

        if raw_token and ':' in raw_token:
            try:
                user_uuid, token = raw_token.split(':', 1)
                cache_key = f'user_token:{user_uuid}'
                if cache.get(cache_key) == token:
                    request.user_uuid = user_uuid
            except Exception:
                pass

        return view_func(self, request, *args, **kwargs)
    return wrapper

def check_merchant_role(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        
        user = get_object_or_404(User, uuid=request.user_uuid)

        if user.role not in ['merchant', 'vip_merchant']:
            return Response({'error': '您不是商家用戶'}, status=403)

        request.user = user
        return view_func(self, request, *args, **kwargs)
    return wrapper

def check_and_downgrade_vip(view_func):
    @wraps(view_func)
    def wrapped_view(self, request, *args, **kwargs):
        user = getattr(request, 'user', None)  
        if user and user.role == 'vip_merchant':
            latest_sub = user.subscriptions.order_by('-ended_at').first()
            if latest_sub and latest_sub.ended_at < timezone.now().date():
                user.role = 'merchant'
                user.is_vip = False
                user.save()
        return view_func(self, request, *args, **kwargs)
    return wrapped_view