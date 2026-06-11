from django.urls import path
from mainapp.views import product_views
from mainapp.views import browsing_views

urlpatterns = [
    # User-facing
    path('shop',                            browsing_views.shop,           name='shop'),
    path('product_detail/<int:prod_id>',    browsing_views.product_detail, name='product_detail'),
    path('product/<int:prod_id>/review',    browsing_views.submit_review,  name='submit_review'),

    # Categories
    path('admin/categories',                        product_views.manage_categories, name='manage_categories'),
    path('admin/categories/add',                    product_views.add_category,      name='add_category'),
    path('admin/categories/<int:cat_id>/edit',      product_views.edit_category,     name='edit_category'),
    path('admin/categories/<int:cat_id>/delete',    product_views.delete_category,   name='delete_category'),
    # Products
    path('admin/products',                          product_views.manage_products,   name='manage_products'),
    path('admin/products/add',                      product_views.add_product,       name='add_product'),
    path('admin/products/<int:prod_id>/edit',       product_views.edit_product,      name='edit_product'),
    path('admin/products/<int:prod_id>/delete',     product_views.delete_product,    name='delete_product'),
    path('admin/products/<int:prod_id>/featured',   product_views.toggle_featured,   name='toggle_featured'),
    path('admin/products/<int:prod_id>/trending',   product_views.toggle_trending,   name='toggle_trending'),
]

