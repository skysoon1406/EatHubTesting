from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utilities.place_api import text_search

class RestaurantSearchView(APIView):
    """
    GET /api/v1/restaurants/search?keyword=xxx&location=xxx&radius=xxx

    回傳 Google Place API 的最多20筆餐廳資料。
    """
    def get(self, request):
        keyword = request.query_params.get('keyword')
        location = request.query_params.get('location')
        radius = request.query_params.get('radius')

        if not keyword or not location or not radius:
            return Response(
                {"error": "請提供 keyword、location、radius"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 預設最多20筆
            data = text_search(keyword, location, radius)
            return Response({"results": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"後端錯誤: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )