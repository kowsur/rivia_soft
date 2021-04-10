from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .models import CustomUser
from .forms import CustomUserLoginForm, CustomUserCreationForm, CustomUserSignupForm

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
