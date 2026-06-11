from django.urls import path
from mainapp.views import message_views

urlpatterns = [
    # User messaging
    path('my_messages',                           message_views.user_inbox,          name='user_inbox'),
    path('my_messages/sent',                      message_views.user_sent,           name='user_sent'),
    path('my_messages/compose',                   message_views.user_compose,        name='user_compose'),
    path('my_messages/<int:msg_id>',              message_views.user_message_thread, name='user_message_thread'),

    # Admin messaging
    path('admin/messages',                        message_views.admin_inbox,         name='admin_inbox'),
    path('admin/messages/sent',                   message_views.admin_sent,          name='admin_sent'),
    path('admin/messages/compose',                message_views.admin_compose,       name='admin_compose'),
    path('admin/messages/<int:msg_id>',           message_views.admin_message_thread,name='admin_message_thread'),
]

