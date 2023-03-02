from django.contrib import admin
from core.admin import admin_site
from .models import Category, Brand


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



