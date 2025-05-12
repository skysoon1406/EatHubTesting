from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utilities.openai_api import openai_api
from utilities.place_api import text_search
from restaurants.models import Restaurant
from django.db import IntegrityError

class SmartSearchView(APIView):
    """
    接收 flavor / mains / staples，呼叫 OpenAI API 組出搜尋關鍵字，
    再依序呼叫 Google Place API 查詢餐廳，若資料庫無此 place_id 則寫入，
    回傳給前端卡片顯示的最多 20 筆。
    """
    def post(self, request):
        # 1. 取得來自前端的三個欄位（皆為 list）
        flavors = request.data.get("flavors", [])
        mains = request.data.get("mains", [])
        staples = request.data.get("staples", [])

        # 基本驗證：三項至少要有一項有值
        if not any([flavors, mains, staples]):
            return Response({"error": "請提供至少一項選擇（口味、主食、主菜）"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 2. 呼叫 OpenAI API 組出關鍵詞
            # keywords = openai_api(flavors, mains, staples)
            keywords = [flavors, mains, staples]
            # keywords = ["泰式", "雞肉", "飯"]
        except Exception as e:
            return Response({"error": f"OpenAI 呼叫失敗: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        results = []  # 最後要回傳的資料
        collected_place_ids = set()  # 避免重複

        try:
            for keyword in keywords:
                # 3. 針對每個關鍵詞呼叫 Google Place API
                place_data = text_search(keyword, location="25.0330,121.5654", radius="5000", count=20)

                for place in place_data:
                    place_id = place.get("placeId")
                    if not place_id or place_id in collected_place_ids:
                        continue  # 跳過空值與重複

                    collected_place_ids.add(place_id)

                    # 4. 寫入資料庫（如果尚未存在）
                    if not Restaurant.objects.filter(place_id=place_id).exists():
                        try:
                            Restaurant.objects.create(
                                name=place.get("name"),
                                address=place.get("address"),
                                google_rating=place.get("rating"),
                                latitude=place.get("latitude"),
                                longitude=place.get("longitude"),
                                place_id=place_id,
                                types=", ".join(place.get("types", [])),
                            )
                        except IntegrityError:
                            pass  # 防止 race condition

                    # 5. 加入回傳卡片
                    results.append({
                        "name": place.get("name"),
                        "address": place.get("address"),
                        "rating": place.get("rating"),
                        "placeId": place_id,
                    })

                    if len(results) >= 20:
                        break

                if len(results) >= 20:
                    break

        except Exception as e:
            return Response({"error": f"Place API 查詢錯誤: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"results": results}, status=status.HTTP_200_OK)
