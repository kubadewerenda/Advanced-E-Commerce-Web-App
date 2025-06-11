from django.db import models
from django.utils.text import slugify
import uuid
from django.conf import settings

# Create your models here.
#-------------------------------------------- Kategoria ----------------------------------------------------
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.parent:
            return f"{self.parent} > {self.name}"
        return self.name
    
#-------------------------------------------- Produkty -----------------------------------------------------
class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(max_length=1500)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    tax_rate = models.DecimalField(
        max_digits=4, decimal_places=2, default=23.00,
        help_text="Stawka VAT w % (np. 23.00, 8.00, 0.00)"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def generate_sku():
        return f"PROD-{uuid.uuid4().hex[:8].upper()}"
    
    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = self.generate_sku() 
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
            unique_slug = self.slug
            counter = 1
            if Product.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{self.slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products_gallery")
    alt_text = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["id"]
    
    def generate_alt(self):
        return f"ZDJ-{self.product.name}"
    
    def save(self, *args, **kwargs):
        if not self.alt_text:
            self.alt_text = self.generate_alt()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.product.name} (Zdjęcie {self.id})"
    
#-------------------------------------------- Koszyk -----------------------------------------------------
class Cart(models.Model):
    cart_code = models.CharField(max_length=11, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="carts",
        null=True,
        blank=True
    )
    cart_code = models.CharField(max_length=64, unique=True, default=uuid.uuid4, editable=False)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"{self.user.email} -> {self.cart_code}"
        return self.cart_code
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} x {self.quantity} -> cart:{self.cart.cart_code}"



