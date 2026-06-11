from django.urls import path
from mainapp.views import event_views

urlpatterns = [
    # Admin
    path('admin/events',                                       event_views.admin_events,         name='admin_events'),
    path('admin/events/add',                                   event_views.add_event,            name='add_event'),
    path('admin/events/<int:event_id>/edit',                   event_views.edit_event,           name='edit_event'),
    path('admin/events/<int:event_id>/delete',                 event_views.delete_event,         name='delete_event'),
    path('admin/events/<int:event_id>/registrations',          event_views.event_registrations,  name='event_registrations'),
    path('admin/events/registrations/<int:reg_id>/approve',    event_views.approve_registration, name='approve_registration'),
    path('admin/events/registrations/<int:reg_id>/reject',     event_views.reject_registration,  name='reject_registration'),

    # User
    path('events',                                             event_views.user_events,          name='user_events'),
    path('events/<int:event_id>',                              event_views.user_event_detail,    name='user_event_detail'),
    path('events/<int:event_id>/register',                     event_views.register_event,       name='register_event'),
    path('my_events',                                          event_views.user_my_events,       name='user_my_events'),
    path('my_events/<int:reg_id>/pass',                        event_views.download_event_pass,  name='download_event_pass'),
]

