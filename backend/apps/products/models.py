from django.db import models
from apps.stores.models import Store
import secrets


class Product(models.Model):
    """Product model."""

    id = models.CharField(primary_key=True, max_length=30, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.JSONField(default=list)  # Array of image URLs
    category = models.CharField(max_length=255)
    in_stock = models.BooleanField(default=True)
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='products'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['in_stock']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.name} - {self.store.name}"

    def save(self, *args, **kwargs):
        if not self.id:
            # Generate CUID-like ID
            self.id = f"cl{secrets.token_urlsafe(16)}"[:30]
        super().save(*args, **kwargs)

    @property
    def discount_percentage(self):
        """Calculate discount percentage."""
        if self.mrp > 0:
            return round(((self.mrp - self.price) / self.mrp) * 100, 2)
        return 0
