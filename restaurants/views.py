from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from utilities.place_api import text_search
from utilities.openai_api import openai_api
from restaurants.models import Restaurant

"""
POST api/v1/restaurants/

body = {
    "flavors": ["日式", "韓式", "清蒸"],
    "mains": ["雞肉", "豬肉", "牛肉"],
    "staples": ["米飯", "麵條"],
    "userLocation": {
        "latitude": 25.0424,
        "longitude": 121.5137
    }
}

API = {
    "result":[
        {
            "name": "麵屋武藏 本店",
            "address": "100台灣台北市中正區忠孝西路一段36號B1",
            "googleRating": 4.3,
            "latitude": 25.0459993,
            "longitude": 121.5170414,
            "types": [
                "restaurant",
                "food",
                "point_of_interest",
                "establishment"
            ],
            "placeId": "ChIJpabH4qapQjQRqmx_I-V8sUg",
            "imageUrl": "https:"
        },
        {
            "name": "鳥人拉麵-西門店",
            ...
        },
        {
            "name": "哥極拉麵 本店",
            ...
        }
        ...
        # 共 10 筆
    ]
}
"""

@api_view(['POST'])
def recommendRestaurants(request):
    data = request.data
    flavors = data['flavors']
    mains = data['mains']
    staples = data['staples']
    # latitude = data['userLocation']['latitude']
    # longitude = data['userLocation']['longitude']
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    location = f'{latitude},{longitude}'
    
    keywords = openai_api(flavors, mains, staples)

    for keyword in keywords:
        result = text_search(keyword, location, radius=800, count=10)

        if len(result) >= 10:
            cleaned_result = [] 

            for p in result:
                if len(cleaned_result) >= 10:
                    break  

                upsert_restaurant(p) 
                cleaned_result.append({
                    'name': p['name'],
                    'address': p['address'],
                    'googleRating': p.get('rating'),
                    'latitude': p['latitude'],
                    'longitude': p['longitude'],
                    'types': p['types'],
                    'placeId': p['placeId']
                })
                
    return Response({'result': cleaned_result}, status=status.HTTP_200_OK)


def upsert_restaurant(place):
    place_id = place.get("placeId")
    if not place_id:
        return

    obj, created = Restaurant.objects.get_or_create(
        place_id=place_id,
        defaults={
            "name": place.get("name"),
            "address": place.get("address"),
            "google_rating": place.get("rating"),
            "latitude": place.get("latitude"),
            "longitude": place.get("longitude"),
            "types": ", ".join(place.get("types", [])),
            "google_photo_reference": place.get("googlePhotoReference"),
        }
    )

    if not created:
        updated = False
        if obj.google_rating != place.get("rating"):
            obj.google_rating = place.get("rating")
            updated = True
        if obj.address != place.get("address"):
            obj.address = place.get("address")
            updated = True
        if obj.name != place.get("name"):
            obj.name = place.get("name")
            updated = True
        if obj.types != ", ".join(place.get("types", [])):
            obj.types = ", ".join(place.get("types", []))
            updated = True
        if updated:
            obj.save()