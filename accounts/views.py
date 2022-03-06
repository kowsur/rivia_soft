from django.shortcuts import render


from companies.views import URLS


def index(request):
    context = {**URLS}
    return render(request, "accounts/index.html", context)

