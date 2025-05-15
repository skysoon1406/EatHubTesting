from rest_framework.decorators import api_view, permission_classes
from users.utils import token_required_fbv
from .models import Review, Restaurant
from .serializers import ReviewSerializer
from rest_framework.response import Response
from rest_framework import status
from utilities.place_api import text_search
from utilities.openai_api import openai_api
from users.models import User

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

@api_view(['POST'])
@token_required_fbv
def create_review(request, restaurant_uuid):
    try:
        restaurant=Restaurant.objects.get(uuid=restaurant_uuid)
    except Restaurant.DoesNotExist:
        return Response({'error':'找不到該餐廳'}, status=status.HTTP_404_NOT_FOUND)
    
    data = request.data.copy()
    user = User.objects.get(uuid=request.user_uuid)

    serializer = ReviewSerializer(data=data)
    print(serializer.fields)
    if serializer.is_valid():
        serializer.save(user=user, restaurant=restaurant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def detail(req):
    pass
