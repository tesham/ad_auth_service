from django.db import models
from django.conf import settings

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL')


class UserSession(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='sessions'
    )
    login_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    refresh_token = models.CharField(max_length=255)

    class Meta:
        db_table = 'user_sessions'
