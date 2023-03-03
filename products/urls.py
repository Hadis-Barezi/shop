from django.urls import path, include
from . import views


app_name = 'products'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('sub/<int:main_cat_id>/', views.SubCategory.as_view(), name='subcategories'),
    path('category_items/<int:sub_cat_id>/', views.CategoryItems.as_view(), name='category_items'),
    # path('details/<int:product_id>/', views.ProductDetails.as_view(), name='product-details'),
    # path('api/v1/', include('product.api.v1.urls'))
]