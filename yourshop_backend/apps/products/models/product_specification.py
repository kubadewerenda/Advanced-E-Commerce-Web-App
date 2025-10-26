from django.db import models
from .product import Product

class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    name = models.CharField('Name', max_length=100)
    value = models.CharField('Value', max_length=255)

    class Meta:
        db_table = 'product_specifications'
        verbose_name = 'Product specification'
        verbose_name_plural = 'Product specifications'
        ordering = ['name']

    def __str__(self):
        return f'{self.product.name} | {self.name} : {self.value}'
