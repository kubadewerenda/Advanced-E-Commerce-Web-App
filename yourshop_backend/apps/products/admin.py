from django.contrib import admin
from .models import ( Product, ProductVariant,
    ProductSpecification, ProductVariantSpecification, ProductVariantImage
)

admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(ProductSpecification)
admin.site.register(ProductVariantSpecification)
admin.site.register(ProductVariantImage)


