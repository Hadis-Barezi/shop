from django.shortcuts import render
from django.views import View
from . import models
from orders import forms


class Home(View):
    template_name = 'products/home.html'
    product_model = models.Product
    num_home_prod = 8

    def get(self, request):
        try:
            products = self.product_model.objects.filter(balance__gt=0)[:self.num_home_prod]
        except:
            return render(request, template_name=self.template_name, context={'products': None})
        else:
            return render(request, template_name=self.template_name, context={'products': products})


class SubCategory(View):
    template_name = 'products/subcategories.html'
    category_model = models.Category

    def get(self, request, main_cat_id):
        subcategories = self.category_model.objects.filter(main_category=main_cat_id)
        return render(request, template_name=self.template_name, context={'subcategories': subcategories})


class CategoryItems(View):
    template_name = 'products/category_items.html'
    product_model = models.Product
    category_model = models.Category

    def get(self, request, sub_cat_id):
        products = self.product_model.objects.filter(category=sub_cat_id)
        subcategory = self.category_model.objects.get(id=sub_cat_id)
        return render(request, template_name=self.template_name, context={'products': products,
                                                                          'subcategory': subcategory.name})


class ProductDetails(View):
    template_name = 'products/product_details.html'
    product_model = models.Product
    form = forms.CartItemQuantityForm()

    def get(self, request, product_id):
        product = self.product_model.objects.get(id=product_id)
        return render(request, template_name=self.template_name, context={'product': product, 'form': self.form})
