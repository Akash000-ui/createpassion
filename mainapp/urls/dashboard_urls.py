from django.urls import path
from mainapp.views import dashboard_views

urlpatterns = [
    path('admin_dashboard', dashboard_views.admin_dashboard, name='admin_dashboard'),
]

