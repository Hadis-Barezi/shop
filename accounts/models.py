from core.models import User, BaseModel
from django.utils.translation import gettext as _
from django.db import models


class ShopUser(User):
    class Meta:
        verbose_name = _("ShopUser")
        verbose_name_plural = _("ShopUsers")


class Address(BaseModel):
    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    province = models.CharField(verbose_name=_("Province"), max_length=50)
    city = models.CharField(verbose_name=_("City"), max_length=50)
    street = models.CharField(verbose_name=_("Street"), max_length=50)
    postal_code = models.CharField(verbose_name=_("Postal code"), max_length=10)
    more_detail = models.TextField(verbose_name=_("More Detail"), null=True, blank=True)
    shop_user = models.ForeignKey('ShopUser', verbose_name=_("Shop user"), on_delete=models.CASCADE,
                                  related_name='addresses')

    def __str__(self):
        return f"{self.province}-{self.city}-{self.street}-{self.more_detail}- post code: {self.postal_code}"
