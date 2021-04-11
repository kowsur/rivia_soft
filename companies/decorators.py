from django.shortcuts import redirect


def allowed_for_staff(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('companies-home')
    return wrapper

def allowed_for_superuser(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('companies-home')
    return wrapper
