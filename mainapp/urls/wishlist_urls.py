from django.urls import path
from mainapp.views import wishlist_views

urlpatterns = [
    path('wishlist',                        wishlist_views.view_wishlist,  name='view_wishlist'),
    path('toggle_wishlist',                 wishlist_views.toggle_wishlist, name='toggle_wishlist'),
    path('wishlist/move/<int:item_id>',     wishlist_views.move_to_cart,   name='move_to_cart'),
]

