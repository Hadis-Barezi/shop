from django.contrib import admin
from core.admin import admin_site
from .models import Category, Brand


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'main_category')
    list_filter = ('id', 'name', 'type', 'main_category')
    search_fields = ('id', 'name', 'type', 'main_category')


# register Category
admin_site.register(Category, CategoryAdmin)



