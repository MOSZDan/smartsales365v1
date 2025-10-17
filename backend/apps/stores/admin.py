from django.contrib import admin
from .models import Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'user', 'status', 'is_active', 'created_at')
    list_filter = ('status', 'is_active')
    search_fields = ('name', 'username', 'email', 'user__email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Info', {'fields': ('user', 'name', 'username', 'description')}),
        ('Contact', {'fields': ('email', 'contact', 'address')}),
        ('Branding', {'fields': ('logo',)}),
        ('Status', {'fields': ('status', 'is_active')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
