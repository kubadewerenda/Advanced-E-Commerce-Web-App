from rest_framework import serializers
from .models import Product, ProductImage, Category, Cart, CartItem
from django.contrib.auth import get_user_model


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "alt_text"]

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ["id", "name", "sku", "slug", "description", "category",
            "price", "discount_price", "stock", "tax_rate", "is_active",
            "created_at", "modified_at", "images"]
        
class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]

class CategorySerializer(serializers.ModelSerializer):
    children = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "children"]