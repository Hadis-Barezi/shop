from django.urls import path
from . import views
from rest_framework.authtoken import views as auth_token_views


urlpatterns = [
    path('register/', views.ShopUserRegisterAPIView.as_view()),
    path('api-token-auth/', auth_token_views.obtain_auth_token),
    path('user_profile/edit/<int:user_id>/', views.EditProfileAPIView.as_view()),
    path('user_profile/change_password/<int:user_id>/', views.ChangePasswordAPIView.as_view())

]