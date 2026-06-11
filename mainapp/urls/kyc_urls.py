from django.urls import path
from mainapp.views import kyc_views

urlpatterns = [
    # Admin
    path('admin/kyc',                          kyc_views.admin_kyc_list,   name='admin_kyc_list'),
    path('admin/kyc/<int:kyc_id>',             kyc_views.admin_kyc_detail, name='admin_kyc_detail'),
    path('admin/kyc/<int:kyc_id>/approve',     kyc_views.approve_kyc,      name='approve_kyc'),
    path('admin/kyc/<int:kyc_id>/reject',      kyc_views.reject_kyc,       name='reject_kyc'),
    # User
    path('my_kyc',                             kyc_views.user_kyc_detail,  name='user_kyc_detail'),
    path('my_kyc/submit',                      kyc_views.user_kyc_submit,  name='user_kyc_submit'),
]

