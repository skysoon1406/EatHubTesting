from rest_framework import serializers
from .models import Restaurant, Review
from users.serializers import SimpleUserSerializer
from promotions.serializers import PromotionSerializer, CouponSerializer
from utilities.cloudinary_upload import upload_to_cloudinary
from django.core.files.base import ContentFile
import uuid

class FullRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

MAX_IMAGE_SIZE = 1 * 1024 * 1024
class ReviewSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    image_url = serializers.URLField(read_only=True)

    class Meta:
        model = Review
        fields = ['uuid', 'user', 'restaurant', 'rating', 'content', 'created_at', 'image_url']
        read_only_fields = ['uuid', 'created_at', 'user', 'restaurant', 'image_url']

    def create(self, validated_data):
        user = self.context['user']
        restaurant = self.context['restaurant']
        request = self.context.get('request')

        if Review.objects.filter(user=user, restaurant=restaurant).exists():
            raise serializers.ValidationError({'detail':'該餐廳已評論過。'})
        
        image_file = request.FILES.get('image')
        if image_file:
            try:   
                image_data = image_file.read()           
                if len(image_data) > MAX_IMAGE_SIZE:
                    raise ValueError('圖片太大，請小於 1MB')
                
                filename = f'review_{uuid.uuid4()}.jpg'
                image_url = upload_to_cloudinary(ContentFile(image_data, name=filename), filename)
                validated_data['image_url'] = image_url
            except Exception as e:
                raise serializers.ValidationError({'image_bytes': f'圖片處理失敗: {str(e)}'})
            
        return Review.objects.create(user=user, restaurant=restaurant, **validated_data)

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        exclude = ['id', 'created_at']

class SimpleReviewSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()

    class Meta:
        model = Review
        fields = ["user", "rating", "content", "created_at", "image_url"]

class SimpleRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name','image_url']

class RestaurantDetailSerializer(serializers.Serializer):
    restaurant = RestaurantSerializer()
    promotion = serializers.SerializerMethodField()
    coupon = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    user_status = serializers.SerializerMethodField()


    def to_representation(self, obj):
        restaurant_data = RestaurantSerializer(obj, context=self.context).data
        return {
            "restaurant": restaurant_data,
            "promotion": self.get_promotion(obj),
            "coupon": self.get_coupon(obj),
            "reviews": self.get_reviews(obj),
            "user_status": self.get_user_status(obj),
    }
    
    def get_promotion(self, obj):
        promotions = obj.promotions.filter(is_archived=False).order_by("-created_at")
        return (
            PromotionSerializer(promotions, many=True).data
            if promotions.exists()
            else None
        )
    
    def get_coupon(self, obj):
        coupon = obj.coupons.filter(is_archived=False).order_by("-started_at").first()
        return CouponSerializer(coupon).data if coupon else None

    def get_reviews(self, obj):
        reviews = obj.reviews.select_related("user").all()
        return (
            SimpleReviewSerializer(reviews, many=True).data
            if reviews.exists()
            else None
        )
    
    def get_user_status(self, obj):
        request = self.context.get('request')
        user_uuid = getattr(request, 'user_uuid', None)

        result = {
            'hasFavorited': False,
            'hasClaimedCoupon': False,
            'hasReviewed': False
        }

        if not user_uuid:
            return result

        result['hasFavorited'] = obj.favorited_by.filter(user__uuid=user_uuid).exists()
        result['hasReviewed'] = obj.reviews.filter(user__uuid=user_uuid).exists()

        coupon = getattr(self, '_coupon', None)
        if coupon:
            result['hasClaimedCoupon'] = coupon.claimed_by.filter(user__uuid=user_uuid).exists()

        return result