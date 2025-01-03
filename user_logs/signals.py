from django.utils.timezone import now
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.contrib.sessions.models import Session
from .models import ActiveUser, UserLoginHistory, FailedLoginAttempts
import json
from django.http import HttpRequest


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request: HttpRequest, **kwargs):
    failed_attempt = FailedLoginAttempts(
        ip_address=request.META.get("HTTP_X_FORWARDED_FOR", 'HTTP_X_FORWARDED_FOR header value is None'),
        device_user_agent=request.META.get("HTTP_USER_AGENT", 'HTTP_USER_AGENT header value is None'),
        credentials=json.dumps(request.POST.dict(), indent=4))
    failed_attempt.save()


@receiver(user_logged_out)
def log_user_logout(sender, request: HttpRequest, user, **kwargs):    
    session = Session.objects.get(pk=request.session.session_key)
    active_user = ActiveUser.objects.get(user=user, session=session)
    login_history = active_user.user_login_history

    # update log out time
    login_history.logged_out_at = now()
    login_history.save()
    
    # clean up
    session.delete()
    active_user.delete()
