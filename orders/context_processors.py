from .cart import Cart
from accounts.models import ShopUser
from . import models


def cart_items(request):
    if request.user.is_authenticated:
        try:
            user = ShopUser.objects.get(id=request.user.id)
            cart = models.TemporaryCart.objects.filter(shop_user=user).get(is_registered=False)
            item_num = len(cart)
        except:
            item_num = 0
    else:
        cart = Cart(request)
        item_num = len(cart)
    return {'item_num': item_num}