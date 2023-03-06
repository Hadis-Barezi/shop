from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from products.models import Product
from .forms import CartItemQuantityForm, DiscountTicketForm
from . import models
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import ShopUser


class ShopCart(View):
    template_name = 'orders/cart.html'
    temp_cart = models.TemporaryCart
    temp_cart_item = models.CartItem
    shop_user_model = ShopUser

    def get(self, request):
        print("000******")
        if request.user.is_authenticated:
            print("111******")
            try:
                print("222******")
                user = self.shop_user_model.objects.get(id=request.user.id)
                print("333******")
                cart = self.temp_cart.objects.filter(shop_user=user).get(is_registered=False)
                print("444******")
            except ObjectDoesNotExist:
                print("555******")
                messages.warning(request, f"cart is Empty", 'warning')
            else:
                print("666******")
                items = self.temp_cart_item.objects.filter(cart=cart)
                print("777******")
                print(items)
                return render(request, template_name=self.template_name, context={'cart': cart, 'items': items})
        else:
            print("888******")
            cart = Cart(request)
            print("999******")
            return render(request, template_name=self.template_name, context={'cart': cart})


class AddToCart(View):
    temp_cart = models.TemporaryCart
    temp_cart_item = models.CartItem
    product_model = Product
    shop_user_model = ShopUser

    def post(self, request, product_id):
        print("0000***************")
        try:
            print("1111****************")
            product = self.product_model.objects.get(id=product_id)
        except ObjectDoesNotExist:
            print("222****************")
            messages.warning(request, f"product with {product_id} not available", 'warning')
        else:
            print("333**************")
            form = CartItemQuantityForm(request.POST)
            print("444**************")
            if form.is_valid():
                cd = form.cleaned_data
                if not product.check_balance(cd['quantity']):
                    messages.warning(request, "Unfortunately the balance is less than you need!", 'warning')
                    print("555**************")
                else:
                    print("666**************")
                    if request.user.is_authenticated:
                        print("*******", request.user.f_name, "*********")
                        with transaction.atomic():
                            print("*******", "start", "*********")
                            user = self.shop_user_model.objects.get(id=request.user.id)
                            print("*******", "start", "*********")
                            cart = self.temp_cart.objects.get_or_create(shop_user=user)
                            print("*******", "middle", "*********")
                            self.temp_cart_item.objects.create(cart=cart[0], product=product, quantity=cd['quantity'])
                            messages.success(request, f"{product.name} added to the cart.", 'success')
                            print("*******", "end", "*********")

                    else:
                        print("777*******++++******")
                        cart = Cart(request)
                        cart.add_to(product, cd['quantity'])
                        messages.success(request, f"{product.name} added to the cart.", 'success')
        finally:
            print("888*******++++******")
            return redirect("products:home")
