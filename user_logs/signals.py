from django.utils.timezone import now
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.contrib.sessions.models import Session
from .models import ActiveUser, UserLoginHistory, FailedLoginAttempts
import json


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    session = Session.objects.get(pk=request.session.session_key)
    logged_in_user_history = UserLoginHistory(user=user, ip_address=request.META.get("REMOTE_ADDR"), device_user_agent=request.META.get("HTTP_USER_AGENT"))
    logged_in_user_history.save()
    active_user = ActiveUser(user_login_history=logged_in_user_history, user=user, session=session)
    active_user.save()


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    failed_attempt = FailedLoginAttempts(ip_address=request.META.get("REMOTE_ADDR"), device_user_agent=request.META.get("HTTP_USER_AGENT"), credentials=json.dumps(credentials, indent=4))
    failed_attempt.save()


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    for active_user in ActiveUser.objects.filter(user=user):
        # removing session
        session = active_user.session
        session.delete()

        # updateing login_history
        login_history = active_user.user_login_history
        login_history.logged_out_at = now()
        login_history.save()
        
        # removing from active user
        active_user.delete()
