from django.db import models
from .user_models import UserProfile
from .product_models import Product


class Wishlist(models.Model):
    user        = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='wishlist_items')
    product     = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} wishlisted {self.product.name}"

    class Meta:
        db_table = 'wishlist'
        unique_together = ('user', 'product')
        ordering = ['-created_at']
