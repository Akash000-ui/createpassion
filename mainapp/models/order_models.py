from django.db import models
from .user_models import UserProfile
from .product_models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Packed', 'Packed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    user                = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='orders')
    order_number        = models.CharField(max_length=50, unique=True)
    order_date          = models.DateTimeField(auto_now_add=True)
    delivery_address    = models.TextField()
    subtotal            = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    delivery_charge     = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_amount        = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status              = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.order_number} by {self.user.get_full_name()}"

    class Meta:
        db_table = 'orders'
        ordering = ['-order_date']


class OrderItem(models.Model):
    order       = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product     = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    size        = models.CharField(max_length=10, null=True, blank=True)
    quantity    = models.PositiveIntegerField(default=1)
    price       = models.DecimalField(max_digits=10, decimal_places=2)  # price at time of order

    def get_item_total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product.name if self.product else 'Deleted Product'} in Order #{self.order.order_number}"

    class Meta:
        db_table = 'order_items'
