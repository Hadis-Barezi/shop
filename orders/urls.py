from django.urls import path
from . import views

app_name = "orders"
urlpatterns = [
    path('cart/', views.ShopCart.as_view(), name="cart"),
    path('cart/add/<int:product_id>/', views.AddToCart.as_view(), name="add_to_cart"),
]