from django.contrib import admin
from.models import MyUser
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Customer_Address


class CustomUserAdmin(UserAdmin):
    model = MyUser
    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('email', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'image')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'user_permissions', 'confirmation_code', 'email_confirmed')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(MyUser, CustomUserAdmin)
admin.site.register(Customer_Address)