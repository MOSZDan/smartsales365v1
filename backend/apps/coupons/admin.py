from django.contrib import admin
from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'for_new_user', 'for_member', 'is_public', 'expires_at', 'is_valid')
    list_filter = ('for_new_user', 'for_member', 'is_public', 'expires_at')
    search_fields = ('code', 'description')
    ordering = ('-created_at',)

    fieldsets = (
        ('Coupon Info', {'fields': ('code', 'description', 'discount')}),
        ('Eligibility', {'fields': ('for_new_user', 'for_member', 'is_public')}),
        ('Validity', {'fields': ('expires_at',)}),
    )

    def is_valid(self, obj):
        return obj.is_valid
    is_valid.boolean = True
