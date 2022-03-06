from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from companies.views import URLS
from companies.decorators import allowed_for_staff, allowed_for_superuser


@allowed_for_staff()
def index(request):
    context = {**URLS}
    return render(request, "accounts/index.html", context)

