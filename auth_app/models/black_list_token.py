from django.db import models
from django.utils import timezone

class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500, unique=True)
    blacklisted_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'blacklisted_tokens'

    def __str__(self):
        return self.token