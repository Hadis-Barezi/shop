from django.db import models
from core.models import User, BaseModel
from django.utils.translation import gettext as _
from django.urls import reverse
from datetime import datetime


class Category(BaseModel):
    class Meta:
        ordering = ('name',)
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    type_choice = [('M', 'Main Category'), ('Sub', 'Sub-Category')]
    name = models.CharField(verbose_name=_('Name'), max_length=100)
    type = models.CharField(verbose_name=_("Type"), max_length=3, choices=type_choice)
    main_category = models.ForeignKey('self', verbose_name=_("Main category"), on_delete=models.CASCADE, null=True, blank=True, related_name="sub_cats")

    def __str__(self):
        return f"{self.name}"


class Brand(BaseModel):
    class Meta:
        ordering = ('name',)
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    name = models.CharField(verbose_name=_("Name"), max_length=50, unique=True)
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)


class Discount(BaseModel):
    class Meta:
        verbose_name = _("Discount")
        verbose_name_plural = _("Discounts")

    type_choice = [('NUM', 'Numeric'), ('PER', 'Percent')]
    type = models.CharField(verbose_name=_('Type'), max_length=3, choices=type_choice)
    created_in = models.DateField(verbose_name=_("Start Date"))
    expired_in = models.DateField(verbose_name=_("End Date"))
    # value is an integer for Numeric and a float for Percent
    value = models.FloatField(verbose_name=_("value"), default=0)
    # -1 means there is no limit count
    count = models.IntegerField(verbose_name=_("Count"), default=-1)

    def __str__(self):
        return f'{self.type}:{self.value}'

    def is_active(self):
        now = datetime.now().date()
        return bool((self.created_in <= now) and (self.expired_in >= now) and (self.count == -1 or self.count > 0))



