from django.contrib import admin
from .models import (
    Category, Product, ProductSpecification, ProductVariant, ProductImage,
    Cart, CartItem, ProductVariantSpecification
)

# ---------------- KATEGORIA ----------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

# --------------- INLINE MODELE --------------
class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1

class ProductVariantSpecificationInline(admin.TabularInline):
    model = ProductVariantSpecification
    extra = 1

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    show_change_link = True 

# ---------------- PRODUKT -------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_active", "created_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductSpecificationInline, ProductVariantInline, ProductImageInline]
    list_filter = ("is_active", "category")
    readonly_fields = ("created_at", "modified_at")

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    inlines = [ProductVariantSpecificationInline]
    list_display = ("product", "size", "color", "price", "sku")

# ---------------- KOSZYK -------------------
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("cart_code", "user", "paid", "created_at")
    search_fields = ("cart_code",)
    list_filter = ("paid",)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity", "added_at")
    search_fields = ("cart__cart_code", "product__name")


