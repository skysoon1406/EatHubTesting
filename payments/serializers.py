from rest_framework import serializers
from payments.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['uuid', 'name', 'plan_type', 'amount', 'interval_days']