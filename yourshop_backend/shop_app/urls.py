from django.urls import path
from . import views

urlpatterns = [
    path("api/products", views.products, name="products"),
    path("api/products/<slug:slug>", views.product_detail, name="product_detail"),
    path("api/categories/", views.categories, name="categories"),
]