from django.contrib import admin
from .models import ActiveUser, FailedLoginAttempts, UserLoginHistory

# Register your models here.
admin.site.register(ActiveUser)
admin.site.register(UserLoginHistory)
admin.site.register(FailedLoginAttempts)
