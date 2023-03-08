from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.ShopUserRegisterAPIView.as_view(), name='register'),
]