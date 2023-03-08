from . import models
from accounts.models import ShopUser
from products.models import Product
CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)  # none or a key-value of session
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def add_to(self, product, quantity):
        product_id = str(product.id)
        self.cart[product_id] = {'quantity': quantity, 'name': product.name, 'unit_price': product.price,
                             'price_after_discount': product.price_after_discount}
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        for item in self.cart.keys():
            self.cart[item]['total_price'] = self.total_item_price(self.cart[item]['quantity'],
                                                                   self.cart[item]['price_after_discount'])
            self.cart[item]['id'] = item
            self.save()
            yield self.cart[item]

    def __len__(self):
        return len(self.cart)

    @staticmethod
    def total_item_price(quantity, unit_price):
        return quantity*unit_price

    @property
    def total_price(self):
        return sum([item.get('total_price') for item in self.cart.values()]) # without tax rate

    def item_remove(self, product_id):
        if str(product_id) in self.cart.keys():
            del(self.cart[str(product_id)])
            self.save()

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()

    def not_empty(self):
        if self.__len__() >= 1:
            return True
        return False

    def temp_cart(self, request):
        """
        add cart to database after user is authenticated
        """
        user = ShopUser.objects.get(id=request.user.id)
        cart = models.TemporaryCart.objects.get_or_create(shop_user=user)[0]
        print(cart)
        for item in self:
            product_id = int(item['id'])
            print(product_id)
            product = Product.objects.get(id=product_id)
            models.CartItem.objects.create(cart=cart, product=product, quantity=item['quantity'])
            print("****")
        self.clear()
        return cart









