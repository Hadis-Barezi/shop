from  django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('register/', views.ShopUserRegister.as_view(), name='register'),
    path('login/', views.ShopUserLogin.as_view(), name='login'),
    path('logout/', views.ShopUserLogout.as_view(), name='logout'),
    path('user_profile/<int:user_id>/', views.ShopUserProfile.as_view(), name='profile'),
    path('user_profile/edit/<int:user_id>/', views.EditShopUserProfile.as_view(), name='edit_profile'),
    path('user_profile/Change_password/<int:user_id>/', views.ChangePassword.as_view(), name='change_password'),
    path('user_profile/address_list/', views.ShopUserAddressList.as_view(), name='address_list'),
    path('user_profile/add_address/', views.AddAddress.as_view(), name='add_address'),
    path('user_profile/add_address/<int:address_id>/', views.EditAddress.as_view(), name='edit_address'),
    path('user_profile/delete_address/<int:address_id>/', views.DeleteAddress.as_view(), name='delete_address'),
    path('user_profile/order_list/<int:shop_user_id>/', views.ShopUserOrderList.as_view(), name='order_list'),

]