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

    def count_update(self):
        if self.is_active() and self.count>0:
            self.count -= 1
            self.save()


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

    @property
    def get_price(self):
        item = OrderItem(order=self.order, product=self.product, quantity=self.quantity, price=0)
        product = Product.objects.get(id=item.product.id)
        if product.discount:
            discount_type = product.discount.type
            if discount_type == 'PER':
                _price = product.price * (1 - product.discount.value) * self.quantity
            else:
                _price = (product.price - product.discount.value) * self.quantity
        else:
            _price = product.price * item.quantity
        return _price

    def save(self, *args, **kwargs):
        self.price = self.get_price
        super(OrderItem, self).save(*args, **kwargs)


class TemporaryCart(BaseModel):
    class Meta:
        verbose_name = _("Temporary Cart")
        verbose_name_plural = _("Temporary Carts")

    shop_user = models.ForeignKey('accounts.ShopUser', verbose_name=_("Shop User"), on_delete=models.CASCADE)
    is_registered = models.BooleanField(default=False, verbose_name=_("Is Registered"))
    created_in = models.DateField(verbose_name=_("Created In"), auto_now_add=True)

    def __str__(self):
        return f"{self.id}:{self.shop_user}"

    def total_price(self):
        return sum([item.total_price() for item in self.items.all()])

    def __len__(self):
        return len(self.items.all())


class CartItem(BaseModel):
    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")

    cart = models.ForeignKey('TemporaryCart', verbose_name=_("Cart"), on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey('products.Product', verbose_name=_("Product"), on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name=_("Quantity"))

    def total_price(self):
        return self.quantity * self.product.price_after_discount

    def __str__(self):
        return f"{self.id}:{self.product}:{self.quantity}"






