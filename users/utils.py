from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
from functools import wraps



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