from ... import models
from rest_framework import serializers


class TemporaryCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TemporaryCart
        fields = "__all__"


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = "__all__"


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
