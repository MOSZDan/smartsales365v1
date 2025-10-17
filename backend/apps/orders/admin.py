from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'store', 'total', 'status', 'is_paid', 'created_at')
    list_filter = ('status', 'is_paid', 'payment_method', 'created_at')
    search_fields = ('id', 'user__email', 'store__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]

    fieldsets = (
        ('Order Info', {'fields': ('user', 'store', 'address')}),
        ('Payment', {'fields': ('total', 'payment_method', 'is_paid')}),
        ('Status', {'fields': ('status',)}),
        ('Coupon', {'fields': ('is_coupon_used', 'coupon')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'subtotal')
    search_fields = ('order__id', 'product__name')
    ordering = ('-order__created_at',)

    def subtotal(self, obj):
        return obj.subtotal
