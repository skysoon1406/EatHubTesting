from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
from functools import wraps

# token驗證裝飾器


def token_required(view_func):
    @wraps(view_func)
    def warpper(self, request, *args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return Response(
                {"error": "請帶入token"}, status=status.HTTP_401_UNAUTHORIZED
            )
        user_uuid = cache.get(token)
        if not user_uuid:
            return Response(
                {"erroe": "token無效或是過期"}, status=status.HTTP_401_UNAUTHORIZED
            )
        request.user_uuid = user_uuid
        return view_func(self, request, *args, **kwargs)

    return warpper
