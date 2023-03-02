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


class Order(BaseModel):
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    status_choices = [('Deliver', 'Delivered'), ('Send', 'Sending'), ('Return', 'Returned'), ('Cancel', 'Canceled')]
    shop_user = models.ForeignKey(ShopUser, verbose_name=_('Shop user'), on_delete=models.DO_NOTHING, related_name='orders')
    tax_rate = models.FloatField(verbose_name=_('Tax Rate'), default=0.1)
    status = models.CharField(verbose_name=_('Status'), max_length=7, choices=status_choices, default='Send')
    date = models.DateField(verbose_name=_('Date'), auto_now=True)
    address = models.TextField(verbose_name=_("Address"))
    # real amount of total price will be calculated on front end and updated
    discount_ticket = models.ForeignKey(DiscountTicket, verbose_name=_('Discount Code'), on_delete=models.DO_NOTHING,
                                        null=True, blank=True, related_name='orders')
    total_price = models.FloatField('Total Price', default=0)

    def __str__(self):
        return f"{self.id}-{self.shop_user}-{self.total_price}"

    def get_total_price(self):
        # items related name for order items
        items = self.items.all()
        total = sum([item.price for item in items])
        if self.discount_ticket and self.discount_ticket.is_active():
            if self.discount_ticket.type == 'PER':
                total *= (1-self.discount_ticket.value)
            elif self.discount_ticket.type == 'NUM':
                total -= self.discount_ticket.value
        self.total_price = total * (1+self.tax_rate)
        self.save()
        return self.total_price


class OrderItem(BaseModel):
    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    order = models.ForeignKey('Order', verbose_name=_('Order'), on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, verbose_name=_('Product'), on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(verbose_name=_('Quantity'))
    price = models.FloatField(verbose_name=_('Price'), default=0)

    def __str__(self):
        return f'{self.product}-{self.quantity}'
