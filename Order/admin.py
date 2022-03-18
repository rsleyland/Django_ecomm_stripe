from django.contrib import admin
from .models import Order, OrderItem


class CustomOrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('owner', 'subtotal', 'total', 'date_added', 'is_paid')
    list_filter = ('owner', 'subtotal', 'total', 'date_added', 'is_paid')
    fieldsets = (
        (None, {'fields': ('owner', 'subtotal', 'total', 'is_paid')}),
    )
    readonly = ['date_added']
    search_fields = ('owner',)
    ordering = ('owner',)



admin.site.register(Order, CustomOrderAdmin)
admin.site.register(OrderItem)