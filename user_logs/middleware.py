from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from .models import ActiveUser, UserLoginHistory


def UserLastSeenLoggerMiddleware(get_response):
    def middleware(request):
        response = get_response(request)
        if not isinstance(request.user, get_user_model()):
            return response
        
        session = Session.objects.get(pk=request.session.session_key)
        user = request.user

        if ActiveUser.objects.filter(session=session, user=user).exists():
            active_user_log = ActiveUser.objects.get(session=session, user=user)
            active_user_log.save()
            user_login_history = active_user_log.user_login_history
            user_login_history.save()
            return response
        
        # Log is not present for the user so create those
        logged_in_user_history = UserLoginHistory(
            user=user,
            ip_address=request.META.get("HTTP_X_FORWARDED_FOR", 'HTTP_X_FORWARDED_FOR header value is None'),
            device_user_agent=request.META.get("HTTP_USER_AGENT", 'HTTP_USER_AGENT header value is None'))
        logged_in_user_history.save()
        
        active_user = ActiveUser(
            user_login_history=logged_in_user_history,
            user=user,
            session=session
        )
        active_user.save()
        
        return response
    return middleware



from django.utils.timezone import now

class UpdateLastSeenMiddleware:
    """
    Middleware to update the last_seen field for authenticated users.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.user.update_last_seen()
        return self.get_response(request)
