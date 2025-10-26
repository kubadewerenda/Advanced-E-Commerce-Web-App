from django.db import models
from apps.common.utils import unique_slugify
from .base_model import BaseModel
from apps.categories.models import Category

class Product(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(max_length=1500)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products'
    )
    tax_rate = models.DecimalField(
        max_digits=4, decimal_places=2, default=23.00,
        help_text='Tax rate in % (23.00, 8.00, 0.00 etc.)'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'products'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
