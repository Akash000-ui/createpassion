from django.contrib import admin
from mainapp.models import (
    UserProfile, ProductCategory, Product, ProductImage, ProductSize,
    Rating, Review, Order, OrderItem, Cart, Wishlist,
    WalletRequest, WalletBalance, BankDetails, KYC,
    Event, EventRegistration, CompanyDocument, Message,
)

admin.site.register(UserProfile)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductSize)
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(WalletRequest)
admin.site.register(WalletBalance)
admin.site.register(BankDetails)
admin.site.register(KYC)
admin.site.register(Event)
admin.site.register(EventRegistration)
admin.site.register(CompanyDocument)
admin.site.register(Message)
