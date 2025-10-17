from django.db import models
from django.conf import settings
import secrets


class Store(models.Model):
    """Store model for multi-vendor e-commerce."""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    id = models.CharField(primary_key=True, max_length=30, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='store'
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    username = models.SlugField(max_length=255, unique=True)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_active = models.BooleanField(default=False)
    logo = models.URLField(max_length=500)
    email = models.EmailField(max_length=255)
    contact = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Store'
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} (@{self.username})"

    def save(self, *args, **kwargs):
        if not self.id:
            # Generate CUID-like ID
            self.id = f"cl{secrets.token_urlsafe(16)}"[:30]
        super().save(*args, **kwargs)
