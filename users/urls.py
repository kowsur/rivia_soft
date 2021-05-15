from django.urls import path
from django.urls.conf import re_path
from .views import login_user, search_users_by_email, search_users_extended, signup_user, logout_user, all_users, get_user_details


urlpatterns = [
    path('', login_user, name='users'),
    # path('signup/', signup_user, name='users_signup'),
    path('login/', login_user, name='users_login'),
    path('logout/', logout_user, name='users_logout'),
    path('details/<int:user_id>/', get_user_details, name='user_details'),
    path('search_email/<str:search_text>/', search_users_by_email, name='search_users_by_email'),
    path('search/', search_users_extended, name='search_users'),
    path('all/', all_users, name='all_users'),
]
