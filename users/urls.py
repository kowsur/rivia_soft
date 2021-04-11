from django.urls import path
from django.urls.conf import re_path
from .views import login_user, search_users_by_email, search_users_extended, signup_user, logout_user


urlpatterns = [
    path('', login_user, name='users'),
    # path('signup/', signup_user, name='users-signup'),
    path('login/', login_user, name='users_login'),
    path('logout/', logout_user, name='users_logout'),
    path('search/<str:search_text>/', search_users_extended, name='search_users'),
    # path('search_email/<str:search_text>/', search_users_by_email, name='search_users_by_email'),

    re_path('.*', login_user, name='users'), #matches anything
]
