from core.models import User, BaseModel
from django.utils.translation import gettext as _


class ShopUser(User):
    class Meta:
        verbose_name = _("ShopUser")
        verbose_name_plural = _("ShopUsers")

