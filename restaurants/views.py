from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from utilities.place_api import text_search
from utilities.openai_api import openai_api
from restaurants.models import Restaurant

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

                upsert_restaurant(p)   # 使用 upsert_restaurant 函数来更新或插入餐厅数据
                cleaned_result.append({
                'name': p['name'],
                'address': p['address'],
                'google_rating': p.get('google_rating'),
                'latitude': p['latitude'],
                'longitude': p['longitude'],
                'types': p['types'],
                'user_ratings_total': p.get('user_ratings_total'),
                'place_id': p['place_id']
            } )
    return Response({'result': cleaned_result}, status=status.HTTP_200_OK)

def detail(req):
    pass

def upsert_restaurant(place): 
    place_id = place.get("place_id")
    if not place_id:
        return

    obj, created = Restaurant.objects.get_or_create(
        place_id=place_id,
        defaults={
            'name': place.get('name'),
            'address': place.get('address'),
            'google_rating': place.get('google_rating'),
            'latitude': place.get('latitude'),
            'longitude': place.get('longitude'),
            'types': ', '.join(place.get('types', [])),
            'user_ratings_total': place.get('user_ratings_total'),
            'google_photo_reference': place.get('google_photo_reference'),
        }
    )

    if not created:
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