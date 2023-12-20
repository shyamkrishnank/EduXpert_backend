from rest_framework import serializers
from .models import Order

class OrderConfirmedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class GetUserOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model= Order
        fields = ['id']