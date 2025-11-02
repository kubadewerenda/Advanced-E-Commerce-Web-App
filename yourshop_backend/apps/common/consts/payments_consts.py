from django.db import models

class PaymentStatus(models.TextChoices):
    NOT_PAID = 'not_paid', 'Not paid'
    AUTHORIZED = 'authorized', 'Authorized'
    PAID = 'paid', 'Paid'
    REFUNDED = 'refunded', 'Refunded'
    FAILED = 'failed', 'Failed'

class PaymentProvider(models.TextChoices):
    STRIPE = 'stripe', 'Stripe'
    PAYU = 'payu', 'PayU'
    P24 = 'p24', 'Przelewy24'
    COD = 'cod', 'Płatność przy odbiorze'