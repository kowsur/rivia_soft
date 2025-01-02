from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    list_filter = ('is_superuser', 'is_staff', 'is_active', 'date_joined')
    fieldsets = (
        ('User Info', {
                        'classes': ('wide',),
                        'fields': ('email', 'password', 'first_name', 'last_name', 'date_joined')
                      }
        ),
        ('Permissions', {
                        'classes': ('wide',),
                        'fields': ('is_superuser', 'is_staff', 'is_active')
                        }
        ),
    )
    add_fieldsets = (
        ('User Info', {
                        'classes': ('wide',),
                        'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'date_joined')
                      }
        ),
        ('Permissions', {
                        'classes': ('wide',),
                        'fields': ('is_superuser', 'is_staff', 'is_active')
                        }
        )
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email','first_name', 'last_name')



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
