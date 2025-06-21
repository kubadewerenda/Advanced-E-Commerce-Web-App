from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .models import Product, ProductImage, Category, Cart, CartItem
from .serializers import ProductSerializer, CategorySerializer, DetailedProductSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Min, F, DecimalField, Case, When
from rest_framework.pagination import PageNumberPagination

# Create your views here.
@api_view(["GET"])
def categories(request):
    categories = Category.objects.filter(parent__isnull=True).prefetch_related("children")# zwraca tylko te ktore nie maja parenta, czyli glowne 
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def products(request):
    q = request.GET.get("q", "")# jesli nie ma to daje ""
    ordering = request.GET.get("ordering")
    category_slug = request.GET.get("category")
    subcategory_slug = request.GET.get("subcategory")
    price_min = request.GET.get("price_min")
    price_max = request.GET.get("price_max")

    products = Product.objects.filter(
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    if category_slug and not subcategory_slug:
        products = products.filter(
            Q(category__slug=category_slug, category__parent__isnull=True) |  # główna kategoria
            Q(category__parent__slug=category_slug)  # wszystkie podkategorie tej kategorii
    )

    if subcategory_slug:
        products = products.filter(category__slug=subcategory_slug, category__parent__isnull=False)

    products = products.annotate(
        min_variant_price=Min(
            Case(
                When(variants__discount_price__isnull=False, then=F("variants__discount_price")),
                default=F("variants__price"),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )
    )

    if price_min:
        try:
            products = products.filter(min_variant_price__gte=float(price_min))
        except ValueError:
            pass

    if price_max:
        try:
            products = products.filter(min_variant_price__lte=float(price_max))
        except ValueError:
            pass
    
    if ordering in ["price", "-price"]:
        products = products.order_by("min_variant_price" if ordering == "price" else "-min_variant_price")
    elif ordering in ["created_at", "-created_at"]:
        products = products.order_by(ordering)
    
    # if price_min:
    #     try:
    #         products = products.filter(price__gte=float(price_min))
    #     except ValueError:
    #         pass

    # if price_max:
    #     try:
    #         products = products.filter(price__lte=float(price_max))
    #     except ValueError:
    #         pass
    
    # if ordering:
    #     allowed_orderings = ["price", "-price", "created_at", "-created_at"]
    #     if ordering in allowed_orderings:
    #         products = products.order_by(ordering)

    #========= PAGINACJA =========
    paginator = PageNumberPagination()
    paginator.page_size = int(request.GET.get("page_size", 2))
    result_page = paginator.paginate_queryset(products, request)

    serializer = ProductSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(["GET"])
def product_detail(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        return Response({"message": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = DetailedProductSerializer(product)
    return Response(serializer.data)


