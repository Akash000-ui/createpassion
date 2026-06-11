from django.urls import path
from mainapp.views import cart_views

urlpatterns = [
    path('cart',                        cart_views.view_cart,      name='view_cart'),
    path('cart/add',                    cart_views.add_to_cart,    name='add_to_cart'),
    path('cart/update/<int:item_id>',   cart_views.update_cart,    name='update_cart'),
    path('cart/remove/<int:item_id>',   cart_views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear',                  cart_views.clear_cart,     name='clear_cart'),
]

