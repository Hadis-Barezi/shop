from django.urls import path
from . import views

app_name = "orders"
urlpatterns = [
    path('cart/', views.ShopCart.as_view(), name="cart"),
    path('cart/add/<int:product_id>/', views.AddToCart.as_view(), name="add_to_cart"),
    path('cart/remove/<str:product_id>/', views.CartItemRemove.as_view(), name='remove_item'),
    path('cart/shipping/', views.OrderShipping.as_view(), name='shipping'),
    path('cart/add_address/', views.AddAddress.as_view(), name='add_address'),
]