from django.contrib import admin
from core.admin import admin_site
from .models import Category, Brand, Discount


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'main_category')
    list_filter = ('id', 'name', 'type', 'main_category')
    search_fields = ('id', 'name', 'type', 'main_category')


# register Category
admin_site.register(Category, CategoryAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('id', 'name')
    search_fields = ('id', 'name')


# register Brand
admin_site.register(Brand, BrandAdmin)


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'value', 'created_in', 'expired_in', 'count')
    list_filter = ('id', 'type', 'value', 'created_in', 'expired_in', 'count')
    search_fields = ('id', 'type', 'value', 'created_in', 'expired_in', 'count')


# register Discount
admin_site.register(Discount, DiscountAdmin)




