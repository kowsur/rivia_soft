from django.contrib import admin
from .models import ActiveUser, FailedLoginAttempts, UserLoginHistory



class UserLoginHistoryAdmin(admin.ModelAdmin):
    model = UserLoginHistory
    list_display = ("user", "ip_address", "device_user_agent", "logged_in_at", "last_seen_at", "logged_out_at", )
    list_filter = ("user", "ip_address", "device_user_agent", "logged_in_at", "last_seen_at", "logged_out_at", )
    search_fields = ("user", "ip_address", "device_user_agent", "logged_in_at", "last_seen_at", "logged_out_at", )
    ordering = ("-logged_in_at", "-last_seen_at")
    

class ActiveUserAdmin(admin.ModelAdmin):
    model = ActiveUser
    list_display = ("user", "session", "last_seen_at", "user_login_history", )
    list_filter = ("user", "session", "last_seen_at", "user_login_history", )
    search_fields = ("user", "session", "last_seen_at", "user_login_history", )
    ordering = ("-last_seen_at", )
    



class FailedLoginAttemptsAdmin(admin.ModelAdmin):
    model = FailedLoginAttempts
    list_display = ("tried_to_log_in_at", "ip_address", "credentials", "device_user_agent", )
    list_filter = ("tried_to_log_in_at", "ip_address", "credentials", "device_user_agent", )
    search_fields = ("tried_to_log_in_at", "ip_address", "credentials", "device_user_agent", )
    ordering = ("-tried_to_log_in_at", )



# Register your models here.
admin.site.register(FailedLoginAttempts, FailedLoginAttemptsAdmin)
admin.site.register(UserLoginHistory, UserLoginHistoryAdmin)
admin.site.register(ActiveUser, ActiveUserAdmin)

