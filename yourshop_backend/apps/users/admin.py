# apps/users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    ordering = ('email',)
    list_display  = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active')
    list_filter   = ('is_staff', 'is_superuser', 'is_active',)
    search_fields = ('email', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Company', {'fields': ('is_company', 'company_name', 'tax_number')}),
        ('Address', {'fields': ('address', 'postal_code', 'city')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions',)
