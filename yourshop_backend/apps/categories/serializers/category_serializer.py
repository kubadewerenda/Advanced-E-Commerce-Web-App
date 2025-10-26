from rest_framework import serializers
from apps.categories.models import Category

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class CategorySerializer(serializers.ModelSerializer):
    children = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'children']
