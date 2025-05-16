from rest_framework import serializers
from .models import Restaurant, Review
from users.serializers import SimpleUserSerializer
from promotions.serializers import PromotionSerializer, CouponSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    image_url = serializers.URLField(source='img_url', required=False)

    class Meta:
        model = Review
        fields = ['uuid', 'user', 'restaurant', 'rating', 'content', 'created_at', 'image_url']
        read_only_fields = ['uuid', 'created_at', 'user', 'restaurant']
    def create(self, validated_data):
        user = self.context['user']
        restaurant = self.context['restaurant']

        if Review.objects.filter(user=user, restaurant=restaurant).exists():
            raise serializers.ValidationError('該餐廳已評論過。')
        return Review.objects.create(user=user, restaurant=restaurant, **validated_data)

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        exclude = ['id', 'created_at']

class SimpleReviewSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()

    class Meta:
        model = Review
        fields = ["user", "rating", "content", "created_at", "img_url"]

class SimpleRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name','image_url']

class RestaurantDetailSerializer(serializers.Serializer):
    restaurant = RestaurantSerializer()
    promotion = serializers.SerializerMethodField()
    coupon = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

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