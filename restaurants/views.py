from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from users.utils import token_required_fbv, token_required_cbv
from .models import Review, Restaurant
from .serializers import ReviewSerializer
from users.models import User, Favorite
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from utilities.place_api import text_search
from utilities.openai_api import openai_api
from .serializers import RestaurantDetailSerializer


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

@api_view(['POST'])
@token_required_fbv
def create_review(request, restaurant_uuid):
    try:
        restaurant = Restaurant.objects.get(uuid=restaurant_uuid)
    except Restaurant.DoesNotExist:
        return Response({'error':'找不到該餐廳'}, status=status.HTTP_404_NOT_FOUND)
    
    user = User.objects.get(uuid =request.user_uuid)

    serializer = ReviewSerializer(data=request.data, context={'user':user, 'restaurant':restaurant})
    if serializer.is_valid():
        serializer.save(user=user, restaurant=restaurant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def detail(req):
    pass

class RestaurantDetailView(APIView):
    def get(self, request, uuid):
        restaurant = get_object_or_404(Restaurant, uuid=uuid)
        serializer = RestaurantDetailSerializer(restaurant)
        return Response({"result": serializer.data})

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

class FavoriteRestaurantView(APIView):
    @token_required_cbv
    def post(self, request, uuid):
        user = get_object_or_404(User, uuid=request.user_uuid)
        restaurant = get_object_or_404(Restaurant, uuid=uuid)

        if Favorite.objects.filter(user=user, restaurant=restaurant).exists():
            return Response({'success': False}, status=status.HTTP_200_OK)

        Favorite.objects.create(user=user, restaurant=restaurant)
        return Response({'success': True}, status=status.HTTP_201_CREATED)
    
    @token_required_cbv
    def delete(self, request, uuid):
        user = get_object_or_404(User, uuid=request.user_uuid)
        restaurant = get_object_or_404(Restaurant, uuid=uuid)

        favorite =  Favorite.objects.filter(user=user, restaurant=restaurant).first()
        
        if favorite:
            favorite.delete()
            return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)
        return Response({'success': False}, status=status.HTTP_200_OK)
