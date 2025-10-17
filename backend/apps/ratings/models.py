from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.products.models import Product
import secrets


class Rating(models.Model):
    """Product rating and review model."""

    id = models.CharField(primary_key=True, max_length=30, editable=False)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    order_id = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Rating'
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
        ordering = ['-created_at']
        unique_together = [['user', 'product', 'order_id']]
        indexes = [
            models.Index(fields=['product', '-created_at']),
            models.Index(fields=['rating']),
        ]

    def __str__(self):
        return f"{self.rating}⭐ - {self.product.name} by {self.user.email}"

    def save(self, *args, **kwargs):
        if not self.id:
            # Generate CUID-like ID
            self.id = f"cl{secrets.token_urlsafe(16)}"[:30]
        super().save(*args, **kwargs)
