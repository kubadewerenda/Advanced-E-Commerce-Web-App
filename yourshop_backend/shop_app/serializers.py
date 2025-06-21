from rest_framework import serializers
from .models import (
    Product, ProductVariant, ProductSpecification,
    ProductImage, Category, ProductVariantSpecification
)
from django.contrib.auth import get_user_model


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "alt_text"]

class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = ["id", "name", "value"]

class ProductVariantSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariantSpecification
        fields = ["id", "name", "value"]

class ProductVariantSerializer(serializers.ModelSerializer):
    specifications = ProductVariantSpecificationSerializer(many=True, read_only=True)
    
    class Meta:
        model = ProductVariant
        fields = [
            "id", "size", "color", "price", "discount_price",
            "stock", "sku", "is_active", "specifications"
        ]

class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    specifications = ProductSpecificationSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField()
    main_variant = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "description", "category",
            "tax_rate", "is_active", "created_at", "modified_at",
            "images", "specifications", "variants", "main_variant"
        ]
    
    def get_main_variant(self, product):
        cheapest = product.variants.filter(is_active=True).first()
        return ProductVariantSerializer(cheapest).data if cheapest else None
    
        
class DetailedProductSerializer(serializers.ModelSerializer):
    specifications = ProductSpecificationSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField()
    related_products = serializers.SerializerMethodField()
    main_variant = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "description", "category", "tax_rate", "is_active", "created_at",
             "images", "specifications", "variants", "main_variant", "related_products"
            ]
    
    def get_related_products(self, product):
        products = Product.objects.filter(category=product.category).exclude(id=product.id)
        serializer = ProductSerializer(products, many=True)
        return serializer.data
    
    def get_main_variant(self, product):
        cheapest = product.variants.filter(is_active=True).first()
        return ProductVariantSerializer(cheapest).data if cheapest else None

        
class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]

class CategorySerializer(serializers.ModelSerializer):
    children = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "children"]