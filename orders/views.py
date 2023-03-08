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
from accounts.forms import CreateUpdateAddressForm


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
                return redirect('products:home')
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
        print(len(cart))
        temp_cart = cart.temp_cart(request)
        print(temp_cart)
        items = temp_cart.items.all()
        addresses = self.address_model.objects.filter(shop_user=request.user.id)
        print(len(cart))
        return render(request, template_name=self.template_name, context={'addresses': addresses, 'cart': temp_cart,
                                                                          'items': items})


class AddAddress(LoginRequiredMixin, View):
    form_class = CreateUpdateAddressForm
    address_model = Address
    template_name = 'accounts/new_address.html'
    user_model = ShopUser

    def get(self, request):
        form = self.form_class()
        return render(request, template_name=self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_address = form.save(commit=False)
            new_address.shop_user = ShopUser.objects.get(id=request.user.id)
            new_address.save()
            messages.success(request, f"A new address Added successfully.", 'success')
            return redirect('orders:shipping')
        return render(request, template_name=self.template_name, context={'form': form})


class EditAddress(LoginRequiredMixin, View):
    form_class = CreateUpdateAddressForm
    address_model = Address
    template_name = 'accounts/edit_address.html'

    def setup(self, request, *args, **kwargs):
        self.address = get_object_or_404(self.address_model, id=kwargs['address_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.id == self.address.shop_user.id:
            messages.error(request, f"you are not allowed", 'danger')
            return redirect('products:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.address)
        return render(request, template_name=self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            self.address.province = cd['province']
            self. address.city = cd['city']
            self.address.street = cd['street'],
            self.address.postal_code = cd['postal_code']
            self.address.more_detail = cd['more_detail']
            self.address.save()
            messages.success(request, f"your address updated successfully.", 'success')
            return redirect('orders:shipping')
        return render(request, template_name=self.template_name, context={'form': form})


class OrderCreate(LoginRequiredMixin, View):
    temp_cart = models.TemporaryCart
    order_model = models.Order
    order_item_model = models.OrderItem
    product_model = Product
    discount_model = models.DiscountTicket
    shop_user_model = ShopUser

    def post(self, request):
        address = request.POST.get('delivery_address')
        discount_code = request.POST.get('code')
        user = ShopUser.objects.get(id=request.user.id)
        try:
            cart = self.temp_cart.objects.filter(shop_user=user).get(is_registered=False)
            items = cart.items.all()
        except:
            messages.warning(request, f'sorry,there is any cart!', 'warning')
            return redirect('products:home')
        else:
            if len(cart):
                with transaction.atomic():
                    order = self.order_model.objects.create(shop_user=user, address=address)
                    if discount_code != "None":
                        try:
                            discount = self.discount_model.objects.get(code=discount_code)
                            if discount.is_active():
                                order.discount_ticket = discount
                                discount.count_update()
                                order.save()
                                messages.info(request, 'Discount code applied.', 'info')
                        except:
                            messages.warning(request, 'Discount Code in not valid!', 'warning')
                    for item in items:
                        # check and update balance
                        if item.product.update_balance(item.quantity):
                            order_item = self.order_item_model(order=order, product=item.product, quantity=item.quantity)
                            order_item.save()
                        else:
                            messages.warning(request, f'sorry,{item.product.name} is not available, more!', 'warning')
                            cart.items.get(id=item.product.id).delete()
                            return redirect('orders:cart')
                    total_with_tax = order.get_total_price()
                    order.save()
                    cart.items.all().delete()
                    cart.delete()
                    messages.success(request, 'Your order was registered successfully.', 'success')
                    messages.info(request, f'order id: {order.id}', 'info')
                    return redirect('products:home')
            messages.warning(request, 'cart is empty.', 'warning')
            return redirect('products:home')







