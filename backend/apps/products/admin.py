from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'store', 'category', 'price', 'mrp', 'in_stock', 'created_at')
    list_filter = ('category', 'in_stock', 'created_at')
    search_fields = ('name', 'description', 'store__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Product Info', {'fields': ('name', 'description', 'category', 'store')}),
        ('Pricing', {'fields': ('mrp', 'price')}),
        ('Images', {'fields': ('images',)}),
        ('Availability', {'fields': ('in_stock',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
