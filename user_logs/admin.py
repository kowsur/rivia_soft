from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.contrib.admin import SimpleListFilter
from django.contrib.sessions.models import Session
from .models import ActiveUser, FailedLoginAttempts, UserLoginHistory


class UserLoginHistoryAdmin(admin.ModelAdmin):
    model = UserLoginHistory
    list_display = ("user", "ip_address", "device_user_agent", "logged_in_at", "last_seen_at", "logged_out_at", )
    list_filter = ("user", "ip_address", "logged_in_at", "last_seen_at", "logged_out_at", )
    search_fields = ("user__email", "ip_address", "device_user_agent", )
    ordering = ("-logged_in_at", "-last_seen_at")
    

class ActiveUserAdmin(admin.ModelAdmin):
    model = ActiveUser
    list_display = ("user", "session", "last_seen_at", "user_login_history", )
    list_filter = ("user", "last_seen_at", )
    search_fields = ("user", "session", )
    ordering = ("-last_seen_at", )
    



class FailedLoginAttemptsAdmin(admin.ModelAdmin):
    model = FailedLoginAttempts
    list_display = ("tried_to_log_in_at", "ip_address", "credentials", "device_user_agent", )
    list_filter = ("tried_to_log_in_at", "ip_address",)
    search_fields = ("ip_address", "credentials", "device_user_agent", )
    ordering = ("-tried_to_log_in_at", )



# Register your models here.
admin.site.register(FailedLoginAttempts, FailedLoginAttemptsAdmin)
admin.site.register(UserLoginHistory, UserLoginHistoryAdmin)
admin.site.register(ActiveUser, ActiveUserAdmin)


# Custom list filter to filter by user in the session
class UserInSessionFilter(SimpleListFilter):
    title = 'user'  # Label for the filter
    parameter_name = 'user'  # URL parameter name for the filter

    def lookups(self, request, model_admin):
        # Return a list of user tuples to display in the filter
        user_model = get_user_model()
        users = user_model.objects.all()
        return [(user.pk, user.pk) for user in users]

    def queryset(self, request, queryset):
        # If a user ID is selected, filter the queryset based on the user ID
        if self.value():
            # can't get the user since session data is encrypted, avoid this for performance
            return queryset.filter(session_data__contains=f'_auth_user_id={self.value()}') 
        return queryset

class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'user', 'expire_date')
    search_fields = ('session_key',)
    # list_filter = (UserInSessionFilter,)

    def user(self, obj):
        """Retrieve the user associated with the session."""
        try:
            user_model = get_user_model()
            data = obj.get_decoded()
            if '_auth_user_id' in data:
                user = user_model.objects.get(pk=data['_auth_user_id'])
                url = reverse('admin:users_customuser_change', args=[user.pk])
                return mark_safe(f"<a href='{url}'>{user}</a>")
        except ValueError:
            return None

admin.site.register(Session, SessionAdmin)
    