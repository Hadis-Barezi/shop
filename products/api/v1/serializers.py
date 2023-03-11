from rest_framework import serializers
from ... import models


class CategorySerializer(serializers.ModelSerializer):
    category_model = models.Category
    sub_categories = serializers.SerializerMethodField()

    class Meta:
        model = models.Category
        fields = ['id', 'name', 'type', 'sub_categories']

    def get_sub_categories(self, obj):
        subs = obj.sub_cats.all()
        ser_data = CategorySerializer(instance=subs, many=True)
        return ser_data.data


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"




