from django.db import models
from .base_model import BaseModel
from django.conf import settings
from apps.shipping.models import DeliveryMethod
from .payment_method import PaymentMethod

class OrderStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PENDING = 'pending', 'Pending'
    PAID = 'paid', 'Paid'
    SHIPPED = 'shipped', 'Shipped',
    COMPLETED = 'completed', 'Completed'
    CANCELED = 'canceled', 'Canceled'

class PaymentStatus(models.TextChoices):
    NOT_PAID = 'not_paid', 'Not paid'
    AUTHORIZED = 'authorized', 'Authorized'
    PAID = 'paid', 'Paid'
    REFUNDED = 'refunded', 'Refunded'
    FAILED = 'failed', 'Failed'

class Order(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.SET_NULL,
        related_name='orders',
        null=True,
        blank=True,
    )

    delivery_method = models.ForeignKey(DeliveryMethod, null=True, blank=True, on_delete=models.SET_NULL, related_name='orders')
    payment_method = models.ForeignKey(PaymentMethod, null=True, blank=True, on_delete=models.SET_NULL, related_name='orders')

    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    payment_status = models.CharField(max_length=20,choices=PaymentStatus, default=PaymentStatus.NOT_PAID)

    # snapshot shipping address
    shipping_first_name = models.CharField(max_length=50)
    shipping_last_name = models.CharField(max_length=80, blank=True)
    shipping_company_name = models.CharField(max_length=500, blank=True)
    shipping_tax_number = models.CharField(max_length=64, blank=True)
    shipping_street = models.CharField(max_length=255)
    shipping_house_number = models.CharField(max_length=30)
    shipping_apartament_number = models.CharField(max_length=30, blank=True)
    shipping_postal_code = models.CharField(max_length=30)
    shipping_city = models.CharField(max_length=150)
    shipping_country = models.CharField(max_length=100, default='Polska')
    shipping_phone = models.CharField(max_length=30, blank=True)
    shipping_email = models.EmailField(max_length=254, blank=True)

    delivery_method_name = models.CharField(max_length=120, blank=True)
    payment_method_name = models.CharField(max_length=120, blank=True)

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
        uid = self.user.id or 'guest'
        return f'Order #{self.id} ({uid})'