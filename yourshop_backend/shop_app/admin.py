from django.contrib import admin
from .models import Product, ProductImage, Category, Cart, CartItem, ProductVariant, ProductAttributeValue, ProductAttribute, ProductVariantAttributeValue

# Register your models here.
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 5

class ProductVariantAttributeValueInline(admin.TabularInline):
    model = ProductVariantAttributeValue
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    show_change_link = True


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductVariantInline]
    list_display = ("name", "category", "is_active")
    search_fields = ("name", "slug")
    list_filter = ("category", "is_active")
    prepopulated_fields = {"slug": ("name",)}

class ProductVariantAdmin(admin.ModelAdmin):
    inlines = [ProductVariantAttributeValueInline]
    list_display = ("product", "sku", "price", "discount_price", "stock", "is_active")
    search_fields = ("product", "sku")
    list_filter = ("product", "is_active")

class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1

class ProductAttributeAdmin(admin.ModelAdmin):
    inlines = [ProductAttributeValueInline]
    list_display = ("name",)



admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(ProductAttributeValue)
admin.site.register(ProductVariantAttributeValue)
admin.site.register(ProductImage)
admin.site.register(Cart)
admin.site.register(CartItem)

