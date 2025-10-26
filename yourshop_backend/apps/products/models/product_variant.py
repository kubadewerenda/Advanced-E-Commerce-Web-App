import uuid
from django.db import models
from .product import Product

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'product_variants'
        ordering = ['price']

    @staticmethod
    def generate_sku():
        return f'PROD-{uuid.uuid4().hex[:8].upper()}'

    def save(self, *args, **kwargs):
        if not self.sku:
            while True:
                candidate = self.generate_sku()
                if not ProductVariant.objects.filter(sku=candidate).exists():
                    self.sku = candidate
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.name} | {self.name}'
