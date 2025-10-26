from rest_framework import serializers
from apps.products.models import (
    Product, ProductVariant, ProductVariantImage,
    ProductSpecification, ProductVariantSpecification
)
from django.db.models import F
from django.db.models.functions import Coalesce

class VariantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariantImage
        fields = ['id', 'image', 'alt_text']

class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = ['id', 'name', 'value']

class ProductVariantSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariantSpecification
        fields = ['id', 'name', 'value']

class ProductShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'tax_rate']

class ProductVariantSerializer(serializers.ModelSerializer):
    product = ProductShortSerializer(read_only=True)
    specifications = ProductVariantSpecificationSerializer(many=True, read_only=True)
    images = VariantImageSerializer(many=True, read_only=True)
    discount_percent = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = [
            'id', 'name', 'price', 'discount_price', 'stock',
            'sku', 'is_active', 'specifications', 'images',
            'discount_percent', 'product'
        ]

    def get_discount_percent(self, v):
        if v.discount_price:
            return round(100 * (v.price - v.discount_price) / v.price)

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    min_variant_price = serializers.SerializerMethodField()
    num_of_promotions = serializers.SerializerMethodField()
    main_variant = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'category',
            'tax_rate', 'is_active', 'created_at', 'modified_at',
            'min_variant_price', 'main_variant', 'num_of_promotions'
        ]
    
    def get_min_variant_price(self, obj):
        return self.context.get('min_price_map', {}).get(obj.id)

    def get_main_variant(self, product):
        cheapest = (
            product.variants.filter(is_active=True)
            .annotate(eff_price=Coalesce('discount_price', 'price'))
            .order_by('eff_price', 'price', 'id') 
            .first()
        )
        return ProductVariantSerializer(cheapest).data if cheapest else None

    def get_num_of_promotions(self, product):
        return product.variants.exclude(discount_price__isnull=True).count()

class DetailedProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    specifications = ProductSpecificationSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    related_products = serializers.SerializerMethodField()
    promotions = serializers.SerializerMethodField()
    main_variant = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'category', 'tax_rate',
            'is_active', 'created_at', 'modified_at',
            'specifications', 'variants', 'main_variant',
            'related_products', 'promotions'
        ]

    def get_related_products(self, product):
        qs = Product.objects.filter(category=product.category).exclude(id=product.id)[:8]
        return ProductSerializer(qs, many=True).data

    def get_main_variant(self, product):
        cheapest = (
            product.variants.filter(is_active=True)
            .annotate(eff_price=Coalesce('discount_price', 'price'))
            .order_by('eff_price', 'price', 'id') 
            .first()
        )
        return ProductVariantSerializer(cheapest).data if cheapest else None

    def get_promotions(self, product):
        promos = []
        for v in product.variants.all():
            if v.discount_price:
                promos.append({'name': v.name or 'Standard'})
        return promos
