from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from utilities.place_api import text_search
from utilities.openai_api import openai_api
from restaurants.models import Restaurant
from utilities.cloudinary_upload import upload_to_cloudinary
from utilities.place_api import get_google_photo

@api_view(['POST'])
def recommendRestaurants(request):
    data = request.data
    flavors = data['flavors']
    mains = data['mains']
    staples = data['staples']
    latitude = data['user_location']['latitude']
    longitude = data['user_location']['longitude']  # 修改 UserLocation 为 user_location


    location = f'{latitude},{longitude}'
    
    keywords = openai_api(flavors, mains, staples)

    cleaned_result = [] 

    for keyword in keywords:
        restaurants_data = text_search(keyword, location, 800, count=10)
        if len(restaurants_data) >= 10: 
            

            for p in restaurants_data:
                if len(cleaned_result) >= 10:
                    break  

                upsert_restaurant(p)  

                db_restaurant = Restaurant.objects.filter(place_id=p['place_id']).first()
                image_url = db_restaurant.image_url if db_restaurant else None

                cleaned_result.append({
                'name': p['name'],
                'address': p['address'],
                'google_rating': p.get('google_rating'),
                'latitude': p['latitude'],
                'longitude': p['longitude'],
                'types': p['types'],
                'user_ratings_total': p.get('user_ratings_total'),                
                'place_id': p['place_id'],
                'image_url': image_url,                
            } )
    return Response({'result': cleaned_result}, status=status.HTTP_200_OK)

def detail(req):
    pass

def upsert_restaurant(place): 
    place_id = place.get("place_id")
    if not place_id:
        return

    photo_ref = place.get('google_photo_reference')
    image_url = None
    

    obj = Restaurant.objects.filter(place_id=place_id).first()

    if obj:
        # 資料已存在，若 image_url 為空，才補抓圖
        if not obj.image_url and photo_ref:
            photo_bytes = get_google_photo(photo_ref)
            if photo_bytes:
                try:
                    print(f"[Uploading Image] for {place_id}")  # 測試階段 確認圖片是否上傳成功 
                    image_url = upload_to_cloudinary(photo_bytes, filename=place_id)
                    obj.image_url = image_url
                    obj.save()
                except Exception as e:
                    print(f"[Image Upload Error] {place_id} - {e}")
                else:
                    print(f"[Image Fetch Failed] {place_id}") # 測試階段 確認圖片是否上傳成功 
    else:
        print(f"[Skip Upload] {place_id} already has image_url") # 測試階段 確認圖片是否上傳成功 

        # 更新其他欄位（選擇性更新）
        updated = False
        if obj.google_rating != place.get('google_rating'):
            obj.google_rating = place.get('google_rating')
            updated = True
        if obj.address != place.get('address'):
            obj.address = place.get('address')
            updated = True
        if obj.name != place.get('name'):
            obj.name = place.get('name')
            updated = True
        if obj.user_ratings_total != place.get('user_ratings_total'):
            obj.user_ratings_total = place.get('user_ratings_total')
            updated = True
        if obj.types != ', '.join(place.get('types', [])):
            obj.types = ', '.join(place.get('types', []))
            updated = True
        if updated:
            obj.save()

        else:
            # 資料不存在，要新建 ➜ 抓圖 + 上傳
            if photo_ref:
                photo_bytes = get_google_photo(photo_ref)
                if photo_bytes:
                    try:
                        image_url = upload_to_cloudinary(photo_bytes, filename=place_id)
                    except Exception as e:
                        print(f"[Image Upload Error] {place_id} - {e}")

            # 新建資料
            Restaurant.objects.create(
                place_id=place_id,
                name=place.get('name'),
                address=place.get('address'),
                google_rating=place.get('google_rating'),
                latitude=place.get('latitude'),
                longitude=place.get('longitude'),
                types=', '.join(place.get('types', [])),
                user_ratings_total=place.get('user_ratings_total'),
                google_photo_reference=photo_ref,
                image_url=image_url
            )

@api_view(['GET'])
def test_upload_image(request):
    photo_ref = request.GET.get('photo_ref')
    place_id = request.GET.get('place_id')

    if not photo_ref or not place_id:
        return Response(
            {"error": "Missing 'photo_ref' or 'place_id' in query string."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 嘗試取得 Google 圖片
    photo_bytes = get_google_photo(photo_ref)
    if not photo_bytes:
        return Response(
            {"error": "Failed to fetch image from Google using given photo_ref."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # 上傳至 Cloudinary
        image_url = upload_to_cloudinary(photo_bytes, filename=place_id)
    except Exception as e:
        return Response(
            {"error": f"Cloudinary upload failed: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response({
        "message": "Image uploaded successfully.",
        "image_url": image_url
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def testRestaurant(request):
    data = request.data
    flavors = data['flavors']
    mains = data['mains']
    staples = data['staples']
    latitude = data['user_location']['latitude']
    longitude = data['user_location']['longitude'] 

    location = f'{latitude},{longitude}'
    
    keywords = openai_api(flavors, mains, staples)

    for keyword in keywords:
        restaurants_data = text_search(keyword, location, 800, count=10)
        if len(result) >= 10: 
            result = [{
                'name': p['name'],
                'address': p['address'],
                'google_rating': p.get('google_rating'),
                'latitude': p['latitude'],
                'longitude': p['longitude'],
                'types': p['types'],
                'place_id': p['place_id'],
                'image_url': p.get('google_photo_reference'),
            } for p in restaurants_data]
            break
    return Response({'result': result}, status=status.HTTP_200_OK)

                    