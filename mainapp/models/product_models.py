from django.db import models
from .user_models import UserProfile


class ProductCategory(models.Model):
    category_name   = models.CharField(max_length=200, unique=True)
    category_image  = models.ImageField(upload_to='category_images/', null=True, blank=True)
    description     = models.TextField(null=True, blank=True)
    status          = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = 'product_categories'
        ordering = ['category_name']
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'


class Product(models.Model):
    GENDER_CHOICES = [
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Unisex', 'Unisex'),
        ('Kids', 'Kids'),
    ]

    name                = models.CharField(max_length=255)
    category            = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, related_name='products')
    brand               = models.CharField(max_length=200, null=True, blank=True)
    model_no            = models.CharField(max_length=100, null=True, blank=True)
    description         = models.TextField(null=True, blank=True)
    price               = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    stock               = models.PositiveIntegerField(default=0)
    color               = models.CharField(max_length=100, null=True, blank=True)
    gender              = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Unisex')
    featured            = models.BooleanField(default=False)
    trending            = models.BooleanField(default=False)
    main_image          = models.ImageField(upload_to='product_images/')
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    def get_discounted_price(self):
        if self.discount_percentage > 0:
            return round(self.price * (1 - self.discount_percentage / 100), 2)
        return self.price

    def get_savings(self):
        return round(self.price - self.get_discounted_price(), 2)

    def is_in_stock(self):
        return self.stock > 0

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(r.rating for r in ratings) / ratings.count(), 1)
        return 0

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']


class ProductImage(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image       = models.ImageField(upload_to='product_images/gallery/')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.name}"

    class Meta:
        db_table = 'product_images'


class ProductSize(models.Model):
    SIZE_CHOICES = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('XXXL', 'XXXL'),
        ('28', '28'),
        ('30', '30'),
        ('32', '32'),
        ('34', '34'),
        ('36', '36'),
        ('38', '38'),
        ('40', '40'),
    ]

    product     = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    size        = models.CharField(max_length=10, choices=SIZE_CHOICES)

    def __str__(self):
        return f"{self.product.name} - {self.size}"

    class Meta:
        db_table = 'product_sizes'
        unique_together = ('product', 'size')


class Rating(models.Model):
    user        = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='ratings')
    product     = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    rating      = models.PositiveSmallIntegerField(default=5)  # 1-5
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} rated {self.product.name}: {self.rating}"

    class Meta:
        db_table = 'product_ratings'
        unique_together = ('user', 'product')


class Review(models.Model):
    user        = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews')
    product     = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    review      = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.get_full_name()} on {self.product.name}"

    class Meta:
        db_table = 'product_reviews'
        unique_together = ('user', 'product')
        ordering = ['-created_at']
