from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from ... import models
from . import serializers
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.response import Response
from rest_framework import status


class CategoryListAPIView(ListAPIView):
    category_model = models.Category
    queryset = category_model.objects.filter(type="M")
    serializer_class = serializers.CategorySerializer


class CategoryProductsAPIView(APIView):
    product_model = models.Product
    category_model = models.Category
    serializer_class = serializers.ProductSerializer

    def get(self, request, cat_id):
        category = get_object_or_404(self.category_model, id= cat_id)
        products = get_list_or_404(self.product_model, category=category)
        ser_data = self.serializer_class(instance=products, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


