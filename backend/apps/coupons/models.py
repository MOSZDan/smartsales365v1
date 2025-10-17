from django.db import models
from django.utils import timezone


class Coupon(models.Model):
    """Coupon/discount code model."""

    code = models.CharField(primary_key=True, max_length=50)
    description = models.TextField()
    discount = models.DecimalField(max_digits=5, decimal_places=2)  # Percentage
    for_new_user = models.BooleanField(default=False)
    for_member = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Coupon'
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} - {self.discount}% off"

    @property
    def is_valid(self):
        """Check if coupon is still valid."""
        return self.expires_at > timezone.now()

    def is_applicable_for_user(self, user, is_new_user=False):
        """Check if coupon is applicable for a specific user."""
        if not self.is_valid:
            return False
        if self.for_new_user and not is_new_user:
            return False
        if self.for_member and is_new_user:
            return False
        return True
