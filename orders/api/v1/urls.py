from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.ShopCartAPIView.as_view()),
    path('cart/add/', views.AddToCartAPIView.as_view()),
    path('cart/remove/<str:product_id>/', views.CartItemRemoveAPIView.as_view()),
    path('cart/shipping/', views.OrderShippingAPIView.as_view()),
    path('detail/<str:order_id>/', views.OrderDetailsAPIView.as_view()),

]
