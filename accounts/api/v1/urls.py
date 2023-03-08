from django.urls import path
from . import views
from rest_framework.authtoken import views as auth_token_views


urlpatterns = [
    path('register/', views.ShopUserRegisterAPIView.as_view(), name='register'),
    path('api-token-auth/', auth_token_views.obtain_auth_token),
]