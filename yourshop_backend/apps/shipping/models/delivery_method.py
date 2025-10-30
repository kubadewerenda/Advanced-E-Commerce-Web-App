from django.db import models
from .base_model import BaseModel

class DeliveryMethod(BaseModel):
    code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    name = models.CharField(max_length=120)

    fixed_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    free_from = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'delivery_methods'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.code and self.name:
            code_provider = self.name.strip().lower().split()
            code = '_'.join(code_provider)

            i=0
            while self.__class__.objects.filter(code=code).exclude(pk=self.pk).exists():
                i += 1
                code += f'_{i}'

            self.code = code
        super().save(*args, **kwargs)

