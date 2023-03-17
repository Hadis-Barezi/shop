from rest_framework.views import APIView
from ... import models, cart
from accounts.models import ShopUser, Address
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from products.models import Product
from django.db import transaction
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.permissions import IsAuthenticated
from accounts.api.v1.serializers import AddressSerializer
from . import permissions


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
            product = get_object_or_404(self.product_model, id=product_id)
            print("****",product,"****")
            user = self.shop_user_model.objects.get(id=request.user.id)
            try:
                user_cart = self.temp_cart.objects.filter(shop_user=user).get(is_registered=False)
                item = user_cart.items.get(product=product)
            except:
                message = "no cart or product!"
            else:
                item.delete()
                message = "The selected item was removed"
        else:
            user_cart = cart.Cart(request)
            user_cart.cart.item_remove(product_id)
            message = "The selected item was removed"
        return Response(data={"message": message})


class OrderShippingAPIView(APIView):
    shop_user_model = ShopUser
    address_model = Address
    discount_model = models.DiscountTicket
    permission_classes = [IsAuthenticated]
    cart_serializer = serializers.CartItemSerializer
    address_serializer = AddressSerializer
    discount_serializer = serializers.DiscountTicketSerializer
    address_discount_serializer = serializers.AddressDiscountSerializer
    temp_cart_class = models.TemporaryCart
    order_model = models.Order
    order_item_model = models.OrderItem
    product_model = Product

    def get(self, request):
        user_cart = cart.Cart(request)
        temp_cart = user_cart.temp_cart(request)
        shop_user = self.shop_user_model.objects.get(id=request.user.id)
        addresses = self.address_model.objects.filter(shop_user=shop_user)
        if len(temp_cart):
            cart_items = temp_cart.items.all()
            cart_ser_data = self.cart_serializer(instance=cart_items, many=True)
            if addresses:
                address_ser_data = self.address_serializer(instance=addresses, many=True)
                return Response(data={"cart": cart_ser_data.data, "addresses": address_ser_data.data},
                                status=status.HTTP_200_OK)
            else:
                return Response(data={"cart": cart_ser_data.data, "addresses": "No Address! Enter an address."},
                                status=status.HTTP_207_MULTI_STATUS)
        message = "EMPTY CART"
        return Response(data={"message": message}, status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        messages = {"messages":[]}
        ser_data = self.address_discount_serializer(data=request.data)
        if ser_data.is_valid():
            shop_user = self.shop_user_model.objects.get(id=request.user.id)
            delivery_address = self.address_model.objects.filter(id=ser_data.validated_data["address_id"])
            discount_code = ser_data.validated_data.get("discount_code")
            if delivery_address[0].shop_user == shop_user:
                try:
                    user_cart = self.temp_cart_class.objects.filter(shop_user=shop_user).get(is_registered=False)
                    items = user_cart.items.all()
                except:
                    message = "Empty Cart"
                    messages["messages"].append(message)
                    return Response(data=message, status=status.HTTP_204_NO_CONTENT)
                else:
                    if len(user_cart):
                        with transaction.atomic():
                            order = self.order_model.objects.create(shop_user=shop_user, address=str(delivery_address))
                            if discount_code:
                                try:
                                    discount = self.discount_model.objects.get(code=discount_code)
                                    if discount.is_active():
                                        order.discount_ticket = discount
                                        discount.count_update()
                                        order.save()
                                        message = "Discount code applied."
                                        messages["messages"].append(message)
                                    else:
                                        message = "Discount code expired"
                                        messages["messages"].append(message)
                                except:
                                    message = 'Input discount Code in not valid!'
                                    messages["messages"].append(message)
                    for item in items:
                        # check and update balance
                        if item.product.update_balance(item.quantity):
                            order_item = self.order_item_model(order=order, product=item.product,
                                                               quantity=item.quantity)
                            order_item.save()
                        else:
                            messages = f'sorry,{item.product.name} is not available, more!'
                            messages["messages"].append(message)
                            user_cart.items.get(id=item.product.id).delete()
                            if len(user_cart) == 0:
                                messages = f'Empty Cart!'
                                messages["messages"].append(message)
                                break
                    total_with_tax = order.get_total_price()
                    order.save()
                    user_cart.items.all().delete()
                    user_cart.delete()
                    message = f'Your order was registered successfully. ORDER ID: {order.id}'
                    messages["messages"].append(message)
            else:
                message = "Delivery_Address Error!"
                messages["messages"].append(message)
            return Response(data=messages, status=status.HTTP_207_MULTI_STATUS)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailsAPIView(APIView):
    user_model = ShopUser
    order_model = models.Order
    permission_classes = [IsAuthenticated, permissions.IsOwner]
    serializer_class = serializers.OrderItemSerializer

    def get(self, request, *args, **kwargs):
        try:
            order = get_object_or_404(self.order_model, id=kwargs['order_id'])
            self.check_object_permissions(request, order)
        except:
            messages = f"order with {kwargs['order_id']} not available"
            return Response({"message": messages}, status=status.HTTP_403_FORBIDDEN)
        else:
            items = order.items.all()
            ser_data = self.serializer_class(instance=items, many=True)
            return Response(data=ser_data.data, status=status.HTTP_200_OK)











