from rest_framework import serializers
from .models import Restaurant, Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = ["user", "rating", "content", "created_at", "image_url"]

class RestaurantDetailSerializer(serializers.ModelSerializer):
    placeId = serializers.CharField(source="place_id")
    googleRating = serializers.FloatField(source="google_rating")
    imageUrl = serializers.URLField(source="img_url", allow_null=True)
    userRatingsTotal = serializers.IntegerField(source="user_ratings_total", allow_null=True)
    openHours = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = [
            "name", "address", "googleRating", "placeId", "imageUrl",
            "latitude", "longitude", "phone", "openHours", "website", "userRatingsTotal"
        ]

    def get_openHours(self, obj):
        return obj.open_hours or {
            "monday": None,
            "tuesday": None,
            "wednesday": None,
            "thursday": None,
            "friday": None,
            "saturday": None,
            "sunday": None
        }
