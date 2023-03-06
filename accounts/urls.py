from  django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('register/', views.ShopUserRegister.as_view(), name='register'),
    path('login/', views.ShopUserLogin.as_view(), name='login'),
    path('logout/', views.ShopUserLogout.as_view(), name='logout'),
]