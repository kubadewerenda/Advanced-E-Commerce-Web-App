from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # to co narazie wyswietlone w panelu admina
    list_display = ("email", "first_name", "last_name", "discount_percent", "is_staff")

    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("discount_percent",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("discount_percent",)}),
    )

    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)