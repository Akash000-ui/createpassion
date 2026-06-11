from django.urls import path
from mainapp.views import profile_views

urlpatterns = [
    # User-facing
    path('user_dashboard',                    profile_views.user_dashboard,       name='user_dashboard'),
    path('my_profile',                        profile_views.update_profile,       name='update_profile'),
    path('my_team',                           profile_views.genealogy_tree,       name='genealogy_tree'),
    path('my_team/<int:target_id>',           profile_views.genealogy_tree,       name='genealogy_tree_node'),
    path('my_team/children/<int:user_id>',    profile_views.genealogy_children,   name='genealogy_children'),
    # Admin user management
    path('admin/users',                           profile_views.manage_users,       name='manage_users'),
    path('admin/users/<int:user_id>',             profile_views.view_user,          name='view_user'),
    path('admin/users/<int:user_id>/toggle',      profile_views.toggle_user_status, name='toggle_user_status'),
    path('admin/users/<int:user_id>/update-rank', profile_views.update_user_rank,   name='update_user_rank'),
    path('admin/users/import-income',              profile_views.import_income,       name='import_income'),
    # FA+ member registration
    path('register_member',                        profile_views.register_member,     name='register_member'),
    path('my_referrals',                           profile_views.my_referrals,        name='my_referrals'),
    path('my_referrals/<int:referred_user_id>/promote-fc', profile_views.promote_to_fc, name='promote_to_fc'),
]

