from django.contrib import admin
from .models import ShopUser
from core.admin import admin_site, MyUserAdmin


class ShopUserAdmin(admin.ModelAdmin):
    pass


admin_site.register(ShopUser, ShopUserAdmin)


