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

    def __str__(self):
        return self.name


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


class Product(BaseModel):
    class Meta:
        ordering = ('name',)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    name = models.CharField(verbose_name=_('name'), max_length=100)
    price = models.FloatField(verbose_name=_('Price'))
    brand = models.ForeignKey('Brand', verbose_name=_("Brand"), on_delete=models.DO_NOTHING, related_name="products")
    category = models.ManyToManyField('Category', verbose_name=_('Category'))
    description = models.TextField(verbose_name=_('Description'), default='No description')
    image = models.ImageField(upload_to='products/%Y/%m/%d/', verbose_name=_("image"))
    # it is assumed that products are countable
    balance = models.IntegerField(verbose_name=_('Balance'))
    discount = models.ForeignKey('Discount', verbose_name=_('Discount'), on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.name}:{self.price}'

    @property
    def price_after_discount(self):
        if self.discount and self.discount.is_active():
            # _discount = Discount.objects.get(id=self.discount.id) # don't need to get
            if self.discount.type == 'PER':
                _price = self.price * (1 - self.discount.value)
            else:
                _price = self.price - self.discount.value
        else:
            _price = self.price
        return _price

    def check_balance(self, quantity):
        if quantity < self.balance:
            return True
        return False

    def update_balance(self, quantity):
        if self.check_balance(quantity):
            self.balance -= quantity
            self.save()
            return True
        return False




