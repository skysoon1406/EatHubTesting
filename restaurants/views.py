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
from restaurants.models import Restaurant
from utilities.cloudinary_upload import upload_to_cloudinary
from utilities.place_api import get_google_photo
from .serializers import RestaurantDetailSerializer


@api_view(['POST'])
def recommendRestaurants(request):
    data = request.data
    flavors = data['flavors']
    mains = data['mains']
    staples = data['staples']
    latitude = data['user_location']['latitude']
    longitude = data['user_location']['longitude']  


    location = f'{latitude},{longitude}'
    
    keywords = openai_api(flavors, mains, staples)

    cleaned_result = [] 

    for keyword in keywords:
        restaurants_data = text_search(keyword, location, 800, count=10)
        if len(restaurants_data) >= 10: 
            

            for place in restaurants_data:
                if len(cleaned_result) >= 10:
                    break  

                upsert_restaurant(place)  

                db_restaurant = Restaurant.objects.filter(place_id=place['place_id']).first()
                image_url = db_restaurant.image_url if db_restaurant else None

                cleaned_result.append({
                'name': place['name'],
                'address': place['address'],
                'google_rating': place.get('google_rating'),
                'latitude': place['latitude'],
                'longitude': place['longitude'],
                'types': place['types'],
                'user_ratings_total': place.get('user_ratings_total'),                
                'place_id': place['place_id'],
                'image_url': image_url,                
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

class RestaurantDetailView(APIView):
    def get(self, request, uuid):
        restaurant = get_object_or_404(Restaurant, uuid=uuid)
        serializer = RestaurantDetailSerializer(restaurant)
        return Response({"result": serializer.data}, context={"request": request})

def upsert_restaurant(place): 
    place_id = place.get("place_id")
    if not place_id:
        return

    photo_ref = place.get('google_photo_reference')
    image_url = None    

    restaurant = Restaurant.objects.filter(place_id=place_id).first()

    if restaurant:
        if not restaurant.image_url and photo_ref:
            photo_bytes = get_google_photo(photo_ref)
            if photo_bytes:
                try:
                    image_url = upload_to_cloudinary(photo_bytes, filename=place_id)
                    restaurant.image_url = image_url
                    restaurant.save()
                except Exception as e:
                    pass
        
        updated = False
        if restaurant.google_rating != place.get('google_rating'):
            restaurant.google_rating = place.get('google_rating')
            updated = True
        if restaurant.address != place.get('address'):
            restaurant.address = place.get('address')
            updated = True
        if restaurant.name != place.get('name'):
            restaurant.name = place.get('name')
            updated = True
        if restaurant.user_ratings_total != place.get('user_ratings_total'):
            restaurant.user_ratings_total = place.get('user_ratings_total')
            updated = True
        if restaurant.types != ', '.join(place.get('types', [])):
            restaurant.types = ', '.join(place.get('types', []))
            updated = True
        if updated:
            restaurant.save()

    else:
        if photo_ref:
            photo_bytes = get_google_photo(photo_ref)
            if photo_bytes:
                try:
                    image_url = upload_to_cloudinary(photo_bytes, filename=place_id)
                except Exception as e:
                    pass

        
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
