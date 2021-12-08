from .models import ActiveUser, UserLoginHistory
from django.contrib.auth import get_user_model


# class UserLastSeenLoggerMiddleware():
#     def __init__(self, get_response) -> None:
#         self.get_response = get_response
    
#     def __call__(self, request):
#         response = self.get_response(request)
#         if isinstance(request.user, get_user_model()):
#             user = request.user
#             active_user_log = ActiveUser.objects.get(user=user)
#             active_user_log.save()
#             user_login_history = active_user_log.user_login_history
#             user_login_history.save()
#         return response

def UserLastSeenLoggerMiddleware(get_response):
    def middleware(request):
        response = get_response(request)
        if isinstance(request.user, get_user_model()):
            user = request.user
            active_user_log = ActiveUser.objects.get(user=user)
            active_user_log.save()
            user_login_history = active_user_log.user_login_history
            user_login_history.save()
        return response
    return middleware
