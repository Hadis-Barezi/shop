from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from products.models import Product
from .forms import CartItemQuantityForm, DiscountTicketForm


class ShopCart(View):
    template_name = 'orders/cart.html'
    discount_ticket_form = DiscountTicketForm

    def get(self, request):
        cart = Cart(request)
        form = self.discount_ticket_form()
        return render(request, template_name=self.template_name, context={'cart': cart, 'form': form})

