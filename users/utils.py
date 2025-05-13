from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
from functools import wraps

# 驗證裝飾器


def token_required(view_func):
    @wraps(view_func)
    def warpper(self, request, *args, **kwargs):
        raw_token = request.COOKIES.get("auth_token")
        print("token", raw_token)
        if not raw_token or ":" not in raw_token:
            return Response(
                {"error": "未提供 token"}, status=status.HTTP_401_UNAUTHORIZED
            )
        user_uuid, token = raw_token.split(":", 1)
        cache_key = f"user_token:{user_uuid}"
        stored_token = cache.get(cache_key)
        print("比對token:", stored_token)

        if stored_token != token:
            return Response(
                {"error": "Token 驗證失敗"}, status=status.HTTP_401_UNAUTHORIZED
            )
        request.user_uuid = user_uuid
        return view_func(self, request, *args, **kwargs)

    return warpper
