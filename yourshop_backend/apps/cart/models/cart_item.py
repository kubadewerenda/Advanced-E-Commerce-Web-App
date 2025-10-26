from django.db import models
from .base_model import BaseModel

class CartItem(BaseModel):
    cart = models.ForeignKey('cart.Cart', on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey('products.ProductVariant', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'cart_items'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.quantity} x {self.variant} in {self.cart.cart_code}'
