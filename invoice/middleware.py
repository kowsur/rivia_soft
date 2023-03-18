from django.shortcuts import redirect, resolve_url
from django.urls import reverse
from pprint import pprint


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.login_url = reverse('users_login')
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        next_url = request.GET.get('next')
        if not next_url:
            next_url = request.POST.get('next')

        if not request.user.is_authenticated and request.path != self.login_url:
            return redirect(f"{self.login_url}?next={next_url or request.path}")
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response