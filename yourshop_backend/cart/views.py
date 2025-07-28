from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from shop_app.models import ProductVariant
from .serializers import CartSerializer, CartItemSerializer, CartNumItemsSerializer

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
    
    cart = Cart.objects.filter(cart_code=cart_code).first() if cart_code else None
    if not cart:
        cart = Cart.objects.create()
        cart_code = cart.cart_code

    cart_item, created = CartItem.objects.get_or_create(cart=cart, variant=variant)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    serializer = CartItemSerializer(cart_item)
    return Response({
        "cart_code": cart_code,
        "data": serializer.data, 
        "message": "Poprawnie stworzono cart item"
        }, status=201)


@api_view(["GET"])
def cart_num_of_items(request):
    cart_code = request.query_params.get("cart_code")
    try:
        cart = Cart.objects.get(cart_code=cart_code, paid=False)
        serializer = CartNumItemsSerializer(cart)
        return Response(serializer.data) 
    except Cart.DoesNotExist:
        return Response({"error": "Nie ma takiego koszyka."}, status=404)

@api_view(["GET"])
def cart(request, cart_code):
    try:
        cart = Cart.objects.get(cart_code=cart_code, paid=False)

        serializer = CartSerializer(cart)
        return Response(serializer.data)
    except Cart.DoesNotExist:
        return Response({"error": "Nie ma takiego koszyka."}, status=404)
    
@api_view(["PATCH"])
def ci_up_quantity(request):
    try:
        cartitem_id = request.data.get("item_id")
        quantity = request.data.get("quantity")
        quantity = int(quantity)
        cartitem = CartItem.objects.get(id=cartitem_id)
        cartitem.quantity = quantity
        cartitem.save()
        serializer = CartItemSerializer(cartitem)
        return Response({"data": serializer.data, "message": "Pomyślnie zaktualizowano ilość!"})
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
@api_view(["POST"])
def ci_delete(request):
    try:
        cartitem_id = request.data.get("item_id")
        cartitem = CartItem.objects.get(id=cartitem_id)
        cartitem.delete()
        return Response({"message": "Usunięto produkt z koszyka!"}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=400) 