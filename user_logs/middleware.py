from django.contrib.auth import get_user_model
from django.db.models import Exception
from .models import ActiveUser, UserLoginHistory


def UserLastSeenLoggerMiddleware(get_response):
    def middleware(request):
        response = get_response(request)
        if isinstance(request.user, get_user_model()):
            user = request.user
            try:
                active_user_log = ActiveUser.objects.get(user=user)
                active_user_log.save()
                user_login_history = active_user_log.user_login_history
                user_login_history.save()
            except Exception:
                pass
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
