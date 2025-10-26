from rest_framework import serializers
from apps.products.serializers.product_serializer import ProductVariantSerializer
from apps.cart.models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    variant = ProductVariantSerializer(read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "variant", "quantity", "total"]

    def get_total(self, obj):
        price = obj.variant.discount_price or obj.variant.price or 0
        return round(obj.quantity * price, 2)
    
class CartNumItemsSerializer(serializers.ModelSerializer):
    num_of_items = serializers.SerializerMethodField()
    sum_total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "cart_code", "num_of_items", "sum_total"]

    def get_num_of_items(self, obj):
        items = obj.items.all()
        total = sum([item.quantity for item in items])
        return total
    
    def get_sum_total(self, cart):
        items = cart.items.all()
        total = sum([(item.variant.discount_price if item.variant.discount_price else item.variant.price) * item.quantity for item in items])
        return total


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    sum_total = serializers.SerializerMethodField()
    num_of_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "cart_code", "items", "sum_total", "num_of_items", "created_at", "modified_at"]

    def get_sum_total(self, cart):
        items = cart.items.all()
        total = sum([(item.variant.discount_price if item.variant.discount_price else item.variant.price) * item.quantity for item in items])
        return total
    
    def get_num_of_items(self, cart):
        items = cart.items.all()
        total = sum([item.quantity for item in items])
        return total
    