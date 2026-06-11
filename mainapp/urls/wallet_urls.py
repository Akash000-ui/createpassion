from django.urls import path
from mainapp.views import wallet_views

urlpatterns = [
    # Admin
    path('admin/wallet_requests',                         wallet_views.admin_wallet_requests,  name='admin_wallet_requests'),
    path('admin/wallet_requests/<int:req_id>/approve',    wallet_views.approve_wallet,         name='approve_wallet'),
    path('admin/wallet_requests/<int:req_id>/reject',     wallet_views.reject_wallet,          name='reject_wallet'),
    path('admin/wallet/credit/<int:user_id>',             wallet_views.admin_credit_wallet,    name='admin_credit_wallet'),
    # User
    path('wallet',                                        wallet_views.user_wallet,            name='user_wallet'),
    path('wallet/request',                                wallet_views.submit_wallet_request,  name='submit_wallet_request'),
]

