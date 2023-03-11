from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListAPIView.as_view()),
    path('categories/products/<int:cat_id>/', views.CategoryProductsAPIView.as_view()),
]