from django.db import models

class OrderStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PENDING = 'pending', 'Pending'
    PAID = 'paid', 'Paid'
    SHIPPED = 'shipped', 'Shipped',
    COMPLETED = 'completed', 'Completed'
    CANCELED = 'canceled', 'Canceled'