from django.shortcuts import render
from django.views import View
from . import models
import random


class Home(View):
    template_name = 'products/home.html'
    product_model = models.Product
    num_home_prod = 9

    def get(self, request):
        products = self.product_model.objects.filter(balance__gt=0)[:self.num_home_prod]

        return render(request, template_name=self.template_name, context={'products': products})


class SubCategory(View):
    template_name = 'products/subcategories.html'
    category_model = models.Category

    def get(self, request, main_cat_id):
        subcategories = self.category_model.objects.filter(main_category=main_cat_id)
        return render(request, template_name=self.template_name, context={'subcategories': subcategories})
