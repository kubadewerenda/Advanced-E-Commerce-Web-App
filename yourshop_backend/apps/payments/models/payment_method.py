from django.db import models
from .base_model import BaseModel
from django.conf import settings
from apps.common.consts.payments_consts import PaymentProvider

class PaymentMethod(BaseModel):
    code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    name = models.CharField(max_length=120)
    
    provider = models.CharField(max_length=25, choices=PaymentProvider.choices)

    #tax
    fee_flat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fee_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # np. 1.50 oznacza 1.5%

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'payment_methods'
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