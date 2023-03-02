from django.contrib import admin
from .models import ShopUser, Address
from core.admin import admin_site, MyUserAdmin


class ShopUserAdmin(admin.ModelAdmin):
    pass


# register ShopUser Model
admin_site.register(ShopUser, ShopUserAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop_user', 'province', 'city', 'postal_code', 'more_detail')
    list_filter = ('shop_user', 'province', 'city')
    search_fields = ('id', 'shop_user', 'postal_code')


# register Address Model
admin_site.register(Address, AddressAdmin)







