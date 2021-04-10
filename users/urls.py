from django.urls import path
from .views import login_user, signup_user, logout_user


urlpatterns = [
    path('', login_user, name='users'),
    # path('signup/', signup_user, name='users-signup'),
    path('login/', login_user, name='users_login'),
    path('logout/', logout_user, name='users_logout'),
]
