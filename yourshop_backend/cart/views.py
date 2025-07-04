from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from shop_app.models import ProductVariant
from .serializers import CartSerializer, CartItemSerializer

# Create your views here.
@api_view(["POST"])
def add_to_cart(request):
    cart_code = request.data.get("cart_code")
    variant_sku = request.data.get("variant_sku")
    quantity = int(request.data.get("quantity", 1))

    if not variant_sku:
        return Response({"error": "Brakuje variant_sku."}, status=400)
    
    try:
        variant = ProductVariant.objects.get(sku=variant_sku)
    except ProductVariant.DoesNotExist:
        return Response({"error": "Nie znaleziono variantu o tym SKU."}, status=404)
    
    cart = Cart.objects.filter(cart_code=cart_code, paid=False).first() if cart_code else None
    if not cart:
        cart = Cart.objects.create()

    cart_item, created = CartItem.objects.get_or_create(cart=cart, variant=variant)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    serializer = CartSerializer(cart)
    return Response({
        "data": serializer.data, 
        "message": "Poprawnie stworzono cart item"
        }, status=201)