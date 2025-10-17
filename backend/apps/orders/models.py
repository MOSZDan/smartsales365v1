from django.db import models
from django.conf import settings
from apps.stores.models import Store
from apps.products.models import Product
from apps.users.models import Address
import secrets


class Order(models.Model):
    """Order model."""

    class OrderStatus(models.TextChoices):
        ORDER_PLACED = 'ORDER_PLACED', 'Order Placed'
        PROCESSING = 'PROCESSING', 'Processing'
        SHIPPED = 'SHIPPED', 'Shipped'
        DELIVERED = 'DELIVERED', 'Delivered'

    class PaymentMethod(models.TextChoices):
        COD = 'COD', 'Cash on Delivery'
        STRIPE = 'STRIPE', 'Stripe'

    id = models.CharField(primary_key=True, max_length=30, editable=False)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.ORDER_PLACED
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='buyer_orders'
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    is_coupon_used = models.BooleanField(default=False)
    coupon = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Order'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['store', '-created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Order {self.id} - {self.user.email}"

    def save(self, *args, **kwargs):
        if not self.id:
            # Generate CUID-like ID
            self.id = f"cl{secrets.token_urlsafe(16)}"[:30]
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Order item model (junction table)."""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'OrderItem'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        unique_together = [['order', 'product']]

    def __str__(self):
        return f"{self.product.name} x{self.quantity} in Order {self.order.id}"

    @property
    def subtotal(self):
        return self.quantity * self.price
