from django.db import models
from django.contrib.sessions.models import Session
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.formats import date_format


class UserLoginHistory(models.Model):
    class Meta:
        verbose_name = _("User Login History")
        verbose_name_plural = _("User Login Histories")
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(verbose_name="Public ip address of device")
    device_user_agent = models.TextField(verbose_name="User Agent")
    logged_in_at = models.DateTimeField(auto_now_add=True)
    last_seen_at = models.DateTimeField(auto_now=True)
    logged_out_at = models.DateTimeField(default=None, null=True)

    def __str__(self) -> str:
        last_seen = date_format(self.last_seen_at, format="SHORT_DATETIME_FORMAT", use_l10n=True)
        login = date_format(self.logged_in_at, format="SHORT_DATETIME_FORMAT", use_l10n=True)
        logout = date_format(self.logged_out_at, format="SHORT_DATETIME_FORMAT", use_l10n=True) if self.logged_out_at!=None else None
        return f"{self.user}; Login: {login}; LastSeen: {last_seen}; Logout: {logout}"


class ActiveUser(models.Model):
    class Meta:
        verbose_name = _("Active User")
        verbose_name_plural = _("Active Users")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    user_login_history = models.ForeignKey(UserLoginHistory, on_delete=models.CASCADE)
    last_seen_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        last_seen = date_format(self.last_seen_at, format="SHORT_DATETIME_FORMAT", use_l10n=True)
        return f"{self.user} last seen {last_seen}"


class FailedLoginAttempts(models.Model):
    class Meta:
        verbose_name = _("Failed User Login History")
        verbose_name_plural = _("Failed User Login Histories")
    
    ip_address = models.GenericIPAddressField(verbose_name="Public IP")
    credentials = models.TextField("Login Credentials", default="")
    extra_info = models.TextField("Extra Info", default="")
    device_user_agent = models.TextField(verbose_name="User Agent", default="")
    tried_to_log_in_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        login_attempt_at = date_format(self.tried_to_log_in_at, format="SHORT_DATETIME_FORMAT", use_l10n=True)
        return f"At {login_attempt_at} from IP: {self.ip_address}"
