from django.db import models
from .product_variant import ProductVariant

class ProductVariantSpecification(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='specifications')
    name = models.CharField('Name', max_length=100)
    value = models.CharField('Value', max_length=255)

    class Meta:
        db_table = 'product_variant_specifications'
        verbose_name = 'Variant specification'
        verbose_name_plural = 'Variant specifications'
        ordering = ['name']

    def __str__(self):
        return f'{self.variant} | {self.name} : {self.value}'
