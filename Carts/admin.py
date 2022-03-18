from django.contrib import admin
from .models import Cart, CartItem

class CustomCartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ('owner', 'subtotal', 'date_modified')
    list_filter = ('owner', 'subtotal', 'date_modified')
    fieldsets = (
        (None, {'fields': ('owner', 'subtotal')}),
    )
    readonly = ['date_modified']
    search_fields = ('owner',)
    ordering = ('owner',)



admin.site.register(Cart, CustomCartAdmin)
admin.site.register(CartItem)
