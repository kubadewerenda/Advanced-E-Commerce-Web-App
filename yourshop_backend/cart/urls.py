from django.urls import path
from . import views

urlpatterns = [
    path("api/add_to_cart/", views.add_to_cart, name="add_to_cart"),
]