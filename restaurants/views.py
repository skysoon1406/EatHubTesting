from rest_framework.decorators import api_view
from rest_framework.response import Response
from utilities.place_api import text_search
from utilities.openai_api import openai_api

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
    latitude = data['userLocation']['latitude']
    longitude = data['userLocation']['longitude']

    location = f'{latitude},{longitude}'
    
    keywords = openai_api(flavors, mains, staples)

    for keyword in keywords:
        result = text_search(keyword, location, 800, count=10)
        if len(result) >= 10: 
            result = [{
                'name': p['name'],
                'address': p['address'],
                'googleRating': p.get('rating'),
                'latitude': p['latitude'],
                'longitude': p['longitude'],
                'types': p['types'],
                'placeId': p['placeId']
            } for p in result]
            break
    return Response({'result': result})