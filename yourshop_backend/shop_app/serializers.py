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
    discount_percent = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductVariant
        fields = [
            "id", "variant_name", "price", "discount_price",
            "stock", "sku", "is_active", "specifications", "discount_percent"
        ]
    
    def get_discount_percent(self,variant):
        if variant.discount_price:
            return round(100 * (variant.price - variant.discount_price) / variant.price)

class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    specifications = ProductSpecificationSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField()
    main_variant = serializers.SerializerMethodField()
    num_of_promotions = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "description", "category",
            "tax_rate", "is_active", "created_at", "modified_at",
            "images", "specifications", "variants", "main_variant", "num_of_promotions"
        ]
    
    def get_main_variant(self, product):
        cheapest = product.variants.filter(is_active=True).first()
        return ProductVariantSerializer(cheapest).data if cheapest else None
    
    def get_num_of_promotions(self, product):
        count = 0
        for v in product.variants.all():
            if v.discount_price:
                count += 1
        return count
    
        
class DetailedProductSerializer(serializers.ModelSerializer):
    specifications = ProductSpecificationSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField()
    related_products = serializers.SerializerMethodField()
    main_variant = serializers.SerializerMethodField()
    promotions = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "description", "category", "tax_rate", "is_active", "created_at",
             "images", "specifications", "variants", "main_variant", "related_products", "promotions"
            ]
    
    def get_related_products(self, product):
        products = Product.objects.filter(category=product.category).exclude(id=product.id)
        serializer = ProductSerializer(products, many=True)
        return serializer.data
    
    def get_main_variant(self, product):
        cheapest = product.variants.filter(is_active=True).first()
        return ProductVariantSerializer(cheapest).data if cheapest else None
    
    def get_promotions(self, product):
        promotions = []

        for v in product.variants.all():
            if v.discount_price:
                variant_promo = {}
                if v.variant_name:
                    variant_promo["name"] = v.variant_name
                # if v.size:
                #     variant_promo["size"] = v.size
                # elif v.color:
                #     variant_promo["color"] = v.color
                else:
                    variant_promo["variant"] = "Standard"
                promotions.append(variant_promo)        
        return promotions

        
class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]

class CategorySerializer(serializers.ModelSerializer):
    children = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "children"]