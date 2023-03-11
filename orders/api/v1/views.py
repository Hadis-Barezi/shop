from rest_framework.views import APIView
from ... import models, cart
from accounts.models import ShopUser
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from products.models import Product
from django.db import transaction
from django.shortcuts import get_object_or_404


class ShopCartAPIView(APIView):
    temp_cart = models.TemporaryCart
    temp_cart_item = models.CartItem
    shop_user_model = ShopUser
    serializer_class = serializers.CartItemSerializer

    def get(self, request):
        if request.user.is_authenticated:
            try:
                user = self.shop_user_model.objects.get(id=request.user.id)
                temp_cart = self.temp_cart.objects.filter(shop_user=user).get(is_registered=False)
            except ObjectDoesNotExist:
                data = {"messages": "cart is Empty!"}
                return Response(data=data, status=status.HTTP_204_NO_CONTENT)
            else:
                items = self.temp_cart_item.objects.filter(cart=temp_cart)
                ser_data = self.serializer_class(instance=items, many=True)
                return Response(data=ser_data.data, status=status.HTTP_200_OK)
        else:
            cart_obj = cart.Cart(request)
            return Response(data=cart_obj.cart, status=status.HTTP_200_OK)


class AddToCartAPIView(APIView):
    temp_cart = models.TemporaryCart
    temp_cart_item = models.CartItem
    product_model = Product
    shop_user_model = ShopUser
    serializer_class = serializers.AddToCartSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            validated_data = ser_data.validated_data
            try:
                product = self.product_model.objects.get(id=validated_data['product_id'])
            except ObjectDoesNotExist:
                message = {"messages": f"product with {validated_data['product_id']} not available"}
                return Response(data=message, status=status.HTTP_204_NO_CONTENT)
            else:
                if not product.check_balance(validated_data['quantity']):
                    message = {"messages": "Unfortunately the balance is less than you need!"}
                    return Response(data=message, status=status.HTTP_204_NO_CONTENT)
                else:
                    if request.user.is_authenticated:
                        with transaction.atomic():
                            user = self.shop_user_model.objects.get(id=request.user.id)
                            user_cart = self.temp_cart.objects.get_or_create(shop_user=user)
                            if user_cart[0].items.filter(product=product).exists():
                                item = user_cart[0].items.get(product=product)
                                item.quantity = validated_data['quantity']
                                item.save()
                            else:
                                self.temp_cart_item.objects.create(cart=user_cart[0], product=product, quantity=validated_data['quantity'])
                            message = {"messages": f"{product.name} added to the cart."}
                            return Response(data=message, status=status.HTTP_200_OK)
                    else:
                        user_cart = cart.Cart(request)
                        user_cart.add_to(product, validated_data['quantity'])
                        message = {"messages": f"{product.name} added to the cart."}
                        return Response(data=message, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemRemoveAPIView(APIView):
    product_model = Product
    shop_user_model = ShopUser
    temp_cart = models.TemporaryCart
    """
    Remove an Item from the Cart.
    """
    def delete(self, request, product_id):
        if request.user.is_authenticated:
            product = get_object_or_404(self.product_model, id= product_id)
            user = self.shop_user_model.objects.get(id=request.user.id)
            user_cart = self.temp_cart.objects.filter(shop_user=user).get(is_registered=False)
            user_cart.items.get(product=product).delete()
        else:
            user_cart = cart.Cart(request)
            user_cart.cart.item_remove(product_id)
        message = "The selected item was removed"
        return Response(data={"message": message})

