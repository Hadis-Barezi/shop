from django.contrib import admin
from .models import User
from django.utils.translation import gettext as _
from django.contrib.auth.models import Group, ContentType, Permission
from django.contrib.auth.admin import UserAdmin
from . import forms
from accounts.models import Address, ShopUser
from products.models import Product, Brand, Discount, Category
from orders.models import Order, OrderItem, DiscountTicket, TemporaryCart, CartItem


class MyAdminSite(admin.AdminSite):
    site_header = _('Online shop administration')
    site_title = _('Online shop Admin panel')
    index_title = _('Admin panel')


admin_site = MyAdminSite()


class MyUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = forms.UserChangeForm
    add_form = forms.UserCreationForm
    readonly_fields = [
        'last_login', 'is_superuser'
    ]

    list_display = ('id', 'phone', 'email', 'is_admin')
    list_filter = ('is_admin',)
    search_fields = ('email', 'phone', 'f_name')
    ordering = ('id',)
    fieldsets = (
        ('Main', {'fields': ('f_name', 'l_name', 'phone', 'email', 'date_of_birth', 'image', 'last_login', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_superuser', 'groups', 'user_permissions')})
    )
    add_fieldsets = (
        ('main', {'fields': ('f_name', 'l_name', 'phone', 'email', 'date_of_birth', 'image',  'password', 'confirm_password')}),
    )

    filter_horizontal = ('groups', 'user_permissions')


admin_site.register(User, MyUserAdmin)
admin_site.register(Group)

# define group
product_manager_group, created = Group.objects.get_or_create(name="product_manager")
operator_group, created = Group.objects.get_or_create(name="operator")
supervisor_group, created = Group.objects.get_or_create(name="supervisor")


# ShopUser model
content_type_user = ContentType.objects.get_for_model(ShopUser)
user_permissions = Permission.objects.filter(content_type=content_type_user)
for perm in user_permissions:
    operator_group.permissions.add(perm)
    if "view" in perm.codename:
        supervisor_group.permissions.add(perm)

# Address Model
content_type_user = ContentType.objects.get_for_model(Address)
address_permissions = Permission.objects.filter(content_type=content_type_user)
for perm in address_permissions:
    operator_group.permissions.add(perm)
    if "view" in perm.codename:
        supervisor_group.permissions.add(perm)


# Category Model
content_type_user = ContentType.objects.get_for_model(Category)
category_permissions = Permission.objects.filter(content_type=content_type_user)
for perm in category_permissions:
    product_manager_group.permissions.add(perm)
    if "view" in perm.codename:
        supervisor_group.permissions.add(perm)

# Brand Model
content_type_user = ContentType.objects.get_for_model(Brand)
brand_permissions = Permission.objects.filter(content_type=content_type_user)
for perm in brand_permissions:
    product_manager_group.permissions.add(perm)
    if "view" in perm.codename:
        supervisor_group.permissions.add(perm)

# Discount Model
content_type_user = ContentType.objects.get_for_model(Discount)
discount_permissions = Permission.objects.filter(content_type=content_type_user)
for perm in discount_permissions:
    product_manager_group.permissions.add(perm)
    if "view" in perm.codename:
        supervisor_group.permissions.add(perm)

# Product Model
content_type_user = ContentType.objects.get_for_model(Product)
product_permissions = Permission.objects.filter(content_type=content_type_user)
for perm in product_permissions:
    product_manager_group.permissions.add(perm)
    if "view" in perm.codename:
        supervisor_group.permissions.add(perm)

# TemporaryCart model
content_type_user = ContentType.objects.get_for_model(TemporaryCart)
user_permissions = Permission.objects.filter(content_type=content_type_user)
for perm in user_permissions:
    operator_group.permissions.add(perm)
    if "view" in perm.codename:
        supervisor_group.permissions.add(perm)

# CartItem model
content_type_user = ContentType.objects.get_for_model(CartItem)
user_permissions = Permission.objects.filter(content_type=content_type_user)
for perm in user_permissions:
    operator_group.permissions.add(perm)
    if "view" in perm.codename:
        supervisor_group.permissions.add(perm)

# DiscountTicket model
content_type_user = ContentType.objects.get_for_model(DiscountTicket)
user_permissions = Permission.objects.filter(content_type=content_type_user)
for perm in user_permissions:
    operator_group.permissions.add(perm)
    if "view" in perm.codename:
        supervisor_group.permissions.add(perm)

# Order model
content_type_user = ContentType.objects.get_for_model(Order)
user_permissions = Permission.objects.filter(content_type=content_type_user)
for perm in user_permissions:
    operator_group.permissions.add(perm)
    if "view" in perm.codename:
        supervisor_group.permissions.add(perm)

# OrderItem model
content_type_user = ContentType.objects.get_for_model(OrderItem)
user_permissions = Permission.objects.filter(content_type=content_type_user)
for perm in user_permissions:
    operator_group.permissions.add(perm)
    if "view" in perm.codename:
        supervisor_group.permissions.add(perm)

