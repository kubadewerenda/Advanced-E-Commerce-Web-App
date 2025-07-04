from rest_framework import serializers
from .models import Cart, CartItem
from shop_app.serializers import ProductVariantSerializer

class CartItemSerializer(serializers.ModelSerializer):
    variant = ProductVariantSerializer(read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "variant", "quantity", "total"]

    def get_total(self, cart_item):
        return cart_item.quantity * cart_item.variant.price

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    sum_total = serializers.SerializerMethodField()
    num_of_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "cart_code", "items", "sum_total", "num_of_items", "created_at", "modified_at"]

    def get_sum_total(self, cart):
        items = cart.items.all()
        total = sum([items.variant.price * item.quantity for item in items])
        return total
    
    def get_num_of_items(self, cart):
        items = cart.items.all()
        total = sum([item.quantity for item in items])
        return total
    