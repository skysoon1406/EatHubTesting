from .models import Review
from rest_framework import serializers

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model= Review
        fields=['uuid', 'user', 'restaurant', 'rating', 'content', 'image_url', 'created_at']
        read_only_fields=['uuid', 'created_at', 'user','restaurant']

    def validate(self, attrs):
        user = self.context['user']
        restaurant = self.context['restaurant']

        if Review.objects.filter(user=user, restaurant=restaurant).exists():
            raise serializers.ValidationError('該餐廳已評論過。')
        
        return attrs