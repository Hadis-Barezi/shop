from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from products.models import Product
from .forms import CartItemQuantityForm, DiscountTicketForm
from . import models
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import ShopUser, Address
from django.contrib.auth.mixins import LoginRequiredMixin


class ShopCart(View):
    template_name = 'orders/cart.html'
    temp_cart = models.TemporaryCart
    temp_cart_item = models.CartItem
    shop_user_model = ShopUser

    def get(self, request):
        if request.user.is_authenticated:
            try:
                user = self.shop_user_model.objects.get(id=request.user.id)
                cart = self.temp_cart.objects.filter(shop_user=user).get(is_registered=False)
            except ObjectDoesNotExist:
                messages.warning(request, f"cart is Empty", 'warning')
            else:
                items = self.temp_cart_item.objects.filter(cart=cart)
                print(items)
                return render(request, template_name=self.template_name, context={'cart': cart, 'items': items})
        else:
            cart = Cart(request)
            return render(request, template_name=self.template_name, context={'cart': cart})


class AddToCart(View):
    temp_cart = models.TemporaryCart
    temp_cart_item = models.CartItem
    product_model = Product
    shop_user_model = ShopUser

    def post(self, request, product_id):
        try:
            product = self.product_model.objects.get(id=product_id)
        except ObjectDoesNotExist:
            messages.warning(request, f"product with {product_id} not available", 'warning')
        else:
            form = CartItemQuantityForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                if not product.check_balance(cd['quantity']):
                    messages.warning(request, "Unfortunately the balance is less than you need!", 'warning')
                else:
                    if request.user.is_authenticated:
                        with transaction.atomic():
                            user = self.shop_user_model.objects.get(id=request.user.id)
                            cart = self.temp_cart.objects.get_or_create(shop_user=user)
                            self.temp_cart_item.objects.create(cart=cart[0], product=product, quantity=cd['quantity'])
                            messages.success(request, f"{product.name} added to the cart.", 'success')

                    else:
                        cart = Cart(request)
                        cart.add_to(product, cd['quantity'])
                        messages.success(request, f"{product.name} added to the cart.", 'success')
        finally:
            return redirect("products:home")


class CartItemRemove(View):
    """
    Remove an Item from the Cart.
    """
    temp_cart = models.TemporaryCart
    temp_cart_item = models.CartItem
    shop_user_model = ShopUser

    def get(self, request, product_id):
        if request.user and request.user.is_authenticated:
            user = self.shop_user_model.objects.get(id=request.user.id)
            cart = self.temp_cart.objects.filter(shop_user=user).get(is_registered=False)
            cart.items.get(id=product_id).delete()
            messages.success(request, f"Selected Product removed!", 'success')
        else:
            cart = Cart(request)
            cart.item_remove(product_id)
        return redirect("orders:cart")


class OrderShipping(LoginRequiredMixin, View):
    address_model = Address
    template_name = 'orders/shipping.html'
    discount_model = models.DiscountTicket

    def get(self, request):
        """"showing address list"""
        cart = Cart(request)
        temp_cart = cart.temp_cart(request)
        items = temp_cart.items.all()
        addresses = self.address_model.objects.filter(shop_user=request.user.id)
        return render(request, template_name=self.template_name, context={'addresses': addresses, 'cart': temp_cart,
                                                                          'items': items})





