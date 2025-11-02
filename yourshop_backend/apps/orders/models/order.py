from django.db import models
from .base_model import BaseModel
from django.conf import settings
from apps.common.consts.orders_consts import OrderStatus
from apps.common.consts.payments_consts import PaymentStatus
from apps.common.consts.shipping_consts import AddressType
from apps.shipping.models import DeliveryMethod
from apps.payments.models import PaymentMethod

class Order(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.SET_NULL,
        related_name='orders',
        null=True,
        blank=True,
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
    email = models.EmailField(max_length=254, blank=True)

    delivery_method = models.ForeignKey(DeliveryMethod, null=True, blank=True, on_delete=models.SET_NULL, related_name='orders')
    payment_method = models.ForeignKey(PaymentMethod, null=True, blank=True, on_delete=models.SET_NULL, related_name='orders')

    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    payment_status = models.CharField(max_length=20,choices=PaymentStatus.choices , default=PaymentStatus.NOT_PAID)

    payment_fee_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    subtotal_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    currency = models.CharField(max_length=10, default='PLN')

    class Meta:
        db_table = 'order'
        ordering = ['-created_at']

    def __str__(self):
        uid = self.user_id or 'guest'
        return f'Order #{self.id} ({uid})'