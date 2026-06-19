from django.urls import path
from mainapp.views.static_pages_views import static_page


urlpatterns = [
    path('pages/<slug:slug>', static_page, name='static_page'),
]
