from django.urls import path
from . import views

urlpatterns = [
    path("api/add_to_cart/", views.add_to_cart, name="add_to_cart"),
    path("api/cart_num_of_items", views.cart_num_of_items, name="cart_num_of_items"),
    path("api/cart/<str:cart_code>/", views.cart, name="cart"),
]