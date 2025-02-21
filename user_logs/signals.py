import json
from pprint import pp
from django.utils.timezone import now
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.contrib.sessions.models import Session
from .models import ActiveUser, UserLoginHistory, FailedLoginAttempts
from django.http import HttpRequest


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request: HttpRequest, **kwargs):
    login_data = request.POST.dict()
    login_data.pop("csrfmiddlewaretoken")

    failed_attempt = FailedLoginAttempts(
        credentials = json.dumps(login_data),
        extra_info = json.dumps({k:v for k,v in request.headers.items()}),
        ip_address = request.headers.get("X_FORWARDED_FOR", '0.0.0.0'), #  0.0.0.0 indicates the reverse proxy didn't forward the IP Addr
        device_user_agent = request.headers.get("USER_AGENT", 'USER_AGENT = None'),
    )
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
