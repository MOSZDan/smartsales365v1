from django.contrib import admin
from .models import Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__email', 'review')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Rating Info', {'fields': ('user', 'product', 'order_id')}),
        ('Review', {'fields': ('rating', 'review')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
