from django.urls import path
from mainapp.views import order_views

urlpatterns = [
    # Admin
    path('admin/orders',                              order_views.admin_orders,        name='admin_orders'),
    path('admin/orders/<int:order_id>',               order_views.admin_order_detail,  name='admin_order_detail'),
    path('admin/orders/<int:order_id>/status',        order_views.update_order_status, name='update_order_status'),
    # User
    path('checkout',                                  order_views.checkout,            name='checkout'),
    path('my_orders',                                 order_views.user_orders,         name='user_orders'),
    path('my_orders/<int:order_id>',                  order_views.user_order_detail,   name='user_order_detail'),
    path('my_orders/<int:order_id>/cancel',           order_views.cancel_order,        name='cancel_order'),
]

