from django.db import models
from .user_models import UserProfile
from .product_models import Product


class Cart(models.Model):
    user        = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='cart_items')
    product     = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_entries')
    size        = models.CharField(max_length=10, null=True, blank=True)
    quantity    = models.PositiveIntegerField(default=1)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def get_item_total(self):
        return self.product.get_discounted_price() * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in cart of {self.user.get_full_name()}"

    class Meta:
        db_table = 'cart'
        unique_together = ('user', 'product', 'size')
        ordering = ['-created_at']
