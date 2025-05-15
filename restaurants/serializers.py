from .models import Review
from rest_framework import serializers

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model= Review
        fields=['uuid', 'user', 'restaurant', 'rating', 'content', 'image_url', 'created_at']
        read_only_fields=['uuid', 'create_at', 'user','restaurant']