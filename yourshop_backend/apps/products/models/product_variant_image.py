from django.db import models
from .product_variant import ProductVariant

class ProductVariantImage(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products_gallery') 
    alt_text = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'product_variant_images'
        ordering = ['id']

    def save(self, *args, **kwargs):
        if not self.alt_text:
            self.alt_text = f'IMG-{self.variant.product.name}-{self.variant.id}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.variant} (Image {self.id})'
