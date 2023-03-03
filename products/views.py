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