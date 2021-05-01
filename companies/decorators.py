from django.contrib import messages
from django.shortcuts import redirect

def allowed_for_staff(message="Sorry! You are not authorized to see this.", redirect_to='home'):
    def outer_decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_staff:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, message)
                return redirect(redirect_to)
        return wrapper
    return outer_decorator

def allowed_for_superuser(message="Sorry! You are not authorized to see this.", redirect_to='companies:home'):
    def outer_decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, message)
                return redirect(redirect_to)
        return wrapper
    return outer_decorator
