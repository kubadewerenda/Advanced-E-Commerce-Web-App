from django.db import models
from .base_model import BaseModel
from django.conf import settings
from apps.common.consts.shipping_consts import AddressType

class ShippingAddress(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shipping_address'
    )

    address_type = models.CharField(max_length=16, choices=AddressType.choices, default=AddressType.PERSONAL)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=80, blank=True)

    company_name = models.CharField(max_length=500, blank=True)
    tax_number = models.CharField(max_length=64, blank=True)

    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=30)
    apartament_number = models.CharField(max_length=30, blank=True)
    postal_code = models.CharField(max_length=30)
    city = models.CharField(max_length=150)
    country = models.CharField(max_length=100, default='Polska')

    phone = models.CharField(max_length=30, blank=True)
    email = models.CharField(blank=True)

    is_default = models.BooleanField(default=False, help_text='Is this your default address?')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'shipping_address'
        ordering = ['-is_default', '-modified_at']

    def save(self, *args, **kwargs):
        if self.is_default:
            self.__class__.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)