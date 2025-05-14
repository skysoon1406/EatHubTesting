from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from utilities.place_api import text_search
from utilities.openai_api import openai_api

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
        restaurants_data = text_search(keyword, location, 800, count=10)
        if len(result) >= 10: 
            result = [{
                'name': p['name'],
                'address': p['address'],
                'googleRating': p.get('google_rating'),
                'latitude': p['latitude'],
                'longitude': p['longitude'],
                'types': p['types'],
                'placeId': p['place_id']
            } for p in restaurants_data]
            break
    return Response({'result': result}, status=status.HTTP_200_OK)

def detail(req):
    pass