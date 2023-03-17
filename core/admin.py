from django.contrib import admin
from .models import User
from django.utils.translation import gettext as _
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from . import forms


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


