from django.urls import path
from mainapp.views import bank_views

urlpatterns = [
    # Admin
    path('admin/bank',                         bank_views.admin_bank_list,   name='admin_bank_list'),
    path('admin/bank/<int:bank_id>',           bank_views.admin_bank_detail, name='admin_bank_detail'),
    path('admin/bank/<int:bank_id>/approve',   bank_views.approve_bank,      name='approve_bank'),
    path('admin/bank/<int:bank_id>/reject',    bank_views.reject_bank,       name='reject_bank'),
    # User
    path('my_bank',                            bank_views.user_bank_detail,   name='user_bank_detail'),
    path('my_bank/submit',                     bank_views.user_bank_submit,   name='user_bank_submit'),
]

