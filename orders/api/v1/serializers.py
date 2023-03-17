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


class DiscountTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DiscountTicket
        fields = ['code',]


class AddressDiscountSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()
    discount_code = serializers.CharField(required=False)


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrderItem
        fields = ['order', 'product', 'quantity', 'price']



