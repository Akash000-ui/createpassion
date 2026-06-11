from django.urls import path
from mainapp.views.auth_views import (
    home, user_register, user_login, user_logout,
    admin_login, admin_logout,
    forgot_password, reset_password,
)

urlpatterns = [
    path('',                 home,           name='home'),
    path('user_register',    user_register,  name='user_register'),
    path('user_login',       user_login,     name='user_login'),
    path('user_logout',      user_logout,    name='user_logout'),
    path('admin_login',      admin_login,    name='admin_login'),
    path('admin_logout',     admin_logout,   name='admin_logout'),
    path('forgot_password',  forgot_password, name='forgot_password'),
    path('reset_password',   reset_password,  name='reset_password'),
]

