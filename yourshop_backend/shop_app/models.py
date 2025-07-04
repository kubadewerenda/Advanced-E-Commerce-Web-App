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
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(max_length=1500)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    tax_rate = models.DecimalField(
        max_digits=4, decimal_places=2, default=23.00,
        help_text="Stawka VAT w % (np. 23.00, 8.00, 0.00)"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
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

class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="specifications")
    name = models.CharField("Nazwa specyfikacji", max_length=100)
    value = models.CharField("Wartość", max_length=255)

    class Meta:
        verbose_name = "Specyfikacja produktu"
        verbose_name_plural = "Specyfikacje produktu"
        ordering = ["name"]

    def __str__(self):
        return f"{self.product.name} | {self.name} : {self.value}"
    

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    variant_name = models.CharField(max_length=100, blank=True, null=True)
    # size = models.CharField("Rozmiar", max_length=100, blank=True, null=True)
    # color = models.CharField("Kolor", max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["price"]

    @staticmethod
    def generate_sku():
        return f"PROD-{uuid.uuid4().hex[:8].upper()}"
    
    def save(self, *args, **kwargs):
        if not self.sku:
            while True:
                sku = self.generate_sku()
                if not ProductVariant.objects.filter(sku=sku).exists():
                    self.sku = sku
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} | {self.variant_name}"

class ProductVariantSpecification(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="specifications")
    name = models.CharField("Nazwa specyfikacji", max_length=100)
    value = models.CharField("Wartość", max_length=255)

    class Meta:
        verbose_name = "Specyfikacja wariantu"
        verbose_name_plural = "Specyfikacje wariantu"
        ordering = ["name"]

    def __str__(self):
        return f"{self.variant} | {self.name} : {self.value}"

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
# class Cart(models.Model):
#     cart_code = models.CharField(max_length=11, unique=True)
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL, 
#         on_delete=models.CASCADE,
#         related_name="carts",
#         null=True,
#         blank=True
#     )
#     paid = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         if self.user:
#             return f"{self.user.email} -> {self.cart_code}"
#         return self.cart_code
    
# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     added_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.product} x {self.quantity} -> cart:{self.cart.cart_code}"



