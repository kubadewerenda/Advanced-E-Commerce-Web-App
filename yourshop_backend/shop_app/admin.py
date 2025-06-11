from django.contrib import admin
from .models import Product, ProductImage, Category

# Register your models here.
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 5

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ("name", "price", "stock", "is_active")
    search_fields = ("name", "sku")

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)