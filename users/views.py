from django.http.response import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize

from .models import CustomUser
from .forms import CustomUserLoginForm, CustomUserCreationForm, CustomUserSignupForm

from .queries import search_CustomUser, search_CustomUser_by_email

# Create your views here.
def signup_user(request):
    context = {}
    context['form']= CustomUserSignupForm()
    context['theme'] = request.COOKIES.get('theme')
    if request.method == 'POST':
        form = CustomUserSignupForm(request.POST)
        context['form'] = form
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user.is_active = True
            user.save()

            user = authenticate(email=email, password=password)
            if user:
                # if authenticated then let the user login
                login(request, user)
                return redirect('home')

            return redirect('companies-home')
    return render(request, 'users/signup.html', context=context)

def login_user(request):
    context = {'form': CustomUserLoginForm()}
    context['theme'] = request.COOKIES.get('theme')
    if request.method=='POST':
        form = CustomUserLoginForm(request.POST)
        context['form'] = form
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            # see if the user can login with the creedentials
            user = authenticate(email=email, password=password)
            if user:
                # if authenticated then let the user login
                login(request, user)
                return redirect('home')
        context['message'] = 'Incorrect email or password.'
    return render(request, 'users/login.html', context=context)

def logout_user(request):
    logout(request)
    return redirect('users_login')

# Content-type to return the search results
content_type = 'application/json'
# serialize the results with the format
serialize_format = 'json'

def serialize_queryset_to_json(queryset):
    data = serialize(queryset=queryset, format=serialize_format)
    return data

@login_required
def search_users_by_email(request, search_text='', limit=-1):
    if request.method=='GET' and request.headers.get('Content-Type')==content_type:
        results = search_CustomUser_by_email(search_text, limit)
        return HttpResponse(serialize_queryset_to_json(results), content_type=content_type)
    raise Http404()

@login_required
def search_users_extended(request, search_text='', limit=-1):
    if request.method=='GET' and request.headers.get('Content-Type')==content_type:
        results = search_CustomUser(search_text, limit)
        return HttpResponse(serialize_queryset_to_json(results), content_type=content_type)
    raise Http404()
