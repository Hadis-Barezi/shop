from django.db import models
from core.models import BaseModel
from django.utils.translation import gettext as _
from products.models import Product
from accounts.models import ShopUser, Address
from datetime import datetime


class DiscountTicket(BaseModel):
    class Meta:
        verbose_name = _("Discount Ticket")
        verbose_name_plural = _("Discount Tickets")

    type_choice = [('NUM', 'Numeric'), ('PER', 'Percent')]
    type = models.CharField(verbose_name=_('Type'), max_length=3, choices=type_choice)
    code = models.CharField(verbose_name=_('Code'), max_length=8, unique=True)
    created_in = models.DateField(verbose_name=_("Start Date"))
    expired_in = models.DateField(verbose_name=_("End Date"))
    value = models.FloatField(verbose_name=_("Value"), default=0)
    # by default there is no count limit
    # -1 means there is no limit count
    count = models.IntegerField(verbose_name=_("Count"), default=-1)

    def __str__(self):
        return f"{self.type}-{self.code}"

    def is_active(self):
        now = datetime.now().date()
        return bool((self.created_in <= now) and (self.expired_in >= now) and (self.count == -1 or self.count > 0))

