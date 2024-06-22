from django.contrib.auth.models import AbstractUser as u
from django.db import models


class User(u):

    name = models.CharField(
        max_length=200, null=True, blank=True
    )

    contact_number = models.CharField(
        max_length=50, null=True, blank=True
    )

    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'