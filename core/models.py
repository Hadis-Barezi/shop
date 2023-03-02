from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext as _
from . import managers


class BaseModel(models.Model):
    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = _("ShopUser")
        verbose_name_plural = _("ShopUsers")

    f_name = models.CharField(verbose_name=_("First Name"), max_length=50)
    l_name = models.CharField(verbose_name=_("Last Name"), max_length=100)
    email = models.EmailField(verbose_name=_("Email"), max_length=255, unique=True)
    phone = models.CharField(verbose_name=_("Phone"), max_length=11, unique=True)
    date_of_birth = models.DateField(verbose_name=_("Date of birth"), null=True, blank=True)
    image = models.ImageField(verbose_name=_("image"), upload_to='shop_user_image/%Y/%m/%d/', null=True, blank=True)
    is_active = models.BooleanField(verbose_name=_("Is Active"), default=True)
    is_admin = models.BooleanField(verbose_name=_("Is Admin"), default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'f_name', 'l_name']
    objects = managers.UserManager()

    def __str__(self):
        return f"{self.f_name} {self.l_name} : {self.phone}"

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def change_password(self, new_password, old_password):
        if self.check_password(old_password):
            self.set_password(new_password)
