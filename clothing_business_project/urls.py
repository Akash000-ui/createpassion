"""
URL configuration for clothing_business_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Auth
    path('', include('mainapp.urls.auth_urls')),
    # Dashboard
    path('', include('mainapp.urls.dashboard_urls')),
    # Profile
    path('', include('mainapp.urls.profile_urls')),
    # Products
    path('', include('mainapp.urls.product_urls')),
    # Cart
    path('', include('mainapp.urls.cart_urls')),
    # Wishlist
    path('', include('mainapp.urls.wishlist_urls')),
    # Orders
    path('', include('mainapp.urls.order_urls')),
    # Wallet
    path('', include('mainapp.urls.wallet_urls')),
    # Bank
    path('', include('mainapp.urls.bank_urls')),
    # KYC
    path('', include('mainapp.urls.kyc_urls')),
    # Events
    path('', include('mainapp.urls.event_urls')),
    # Documents
    path('', include('mainapp.urls.document_urls')),
    # Messaging
    path('', include('mainapp.urls.message_urls')),
    # Reports
    path('', include('mainapp.urls.report_urls')),
    # Static Pages
    path('', include('mainapp.urls.static_pages_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
