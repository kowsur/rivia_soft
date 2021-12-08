from django.db import models
from django.utils.timezone import now
from django.contrib.sessions.models import Session
from django.conf import settings
from django.utils.translation import gettext_lazy as _


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
        return f"{self.user} logged in at {self.logged_in_at} last seen at {self.last_seen_at} logged out at {self.logged_out_at}"


class ActiveUser(models.Model):
    class Meta:
        verbose_name = _("Active User")
        verbose_name_plural = _("Active Users")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    user_login_history = models.ForeignKey(UserLoginHistory, on_delete=models.CASCADE)
    last_seen_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user} last seen at {self.last_seen_at}"


class FailedLoginAttempts(models.Model):
    class Meta:
        verbose_name = _("Failed User Login History")
        verbose_name_plural = _("Failed User Login Histories")
    
    ip_address = models.GenericIPAddressField(verbose_name="Public ip address of device")
    credentials = models.TextField()
    device_user_agent = models.TextField(verbose_name="User Agent")
    tried_to_log_in_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"At {self.tried_to_log_in_at} from {self.ip_address} ip using device {self.device_user_agent} provided creedentials: {self.credentials}"
