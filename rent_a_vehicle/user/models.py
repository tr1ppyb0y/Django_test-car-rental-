import datetime

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone


USER_TYPE = (
    ('rener', 'renter'),
    ('owner', 'owner'),
    ('admin', 'admin')
)


class User(AbstractUser):
    username = models.CharField(max_length=150, blank=False, null=False, unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE, default='renter')
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    user_created = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class UserLoginLogs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=50, choices=USER_TYPE, default='renter')
    login_at = models.DateTimeField()

    def save(self, *args, **kwargs) -> None:
        self.login_at = datetime.datetime.now(tz=timezone.utc)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username
