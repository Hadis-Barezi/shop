from django.contrib import admin
from core.admin import admin_site
from .models import DiscountTicket, OrderItem, Order, TemporaryCart, CartItem


class DiscountTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'created_in', 'expired_in', 'value', 'count')
    list_filter = ('id', 'expired_in', 'created_in')
    search_fields = ('id', 'type', 'value', 'expired_in', 'created_in')


# register DiscountTicket
admin_site.register(DiscountTicket, DiscountTicketAdmin)


class OrderItemInLine(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInLine,
    ]


# register Order and OrderItem
admin_site.register(Order, OrderAdmin)


# class CartItemInLine(admin.TabularInline):
#     model = CartItem
#
#
# class TemporaryCartAdmin(admin.ModelAdmin):
#     inlines = [
#         CartItemInLine,
#     ]
#
#
# # register TemporaryCart and TemporaryCartAdmin
# admin_site.register(TemporaryCart, TemporaryCartAdmin)
