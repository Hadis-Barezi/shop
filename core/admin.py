from django.contrib import admin
from .models import User
from django.utils.translation import gettext as _
from django.contrib.auth.models import Group


class MyAdminSite(admin.AdminSite):
    site_header = _('Online shop administration')
    site_title = _('Online shop Admin panel')
    index_title = _('Admin panel')


admin_site = MyAdminSite()
admin_site.register(User)
admin_site.register(Group)
