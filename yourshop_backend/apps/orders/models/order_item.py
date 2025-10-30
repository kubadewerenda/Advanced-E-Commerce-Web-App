from django.db import models
from .base_model import BaseModel
from .order import Order

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_id = models.PositiveIntegerField()
    variant_id = models.PositiveIntegerField()
    product_name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, blank=True)

    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    line_total = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'order_item'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'OrderItem #{self.id} -> Order #{self.order.id}'