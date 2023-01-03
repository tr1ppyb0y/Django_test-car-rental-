from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

USER_TYPE = (
    ('rener', 'renter'),
    ('owner', 'owner'),
)

class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    username = models.CharField(max_length=150, blank=False, null=False, unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE, default='renter')
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    user_created = models.DateTimeField(auto_now_add=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def save(self, *args, **kwargs):
        self.set_password(self.password)
        return super().save(*args, **kwargs)



class UserLoginLogs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=50, choices=USER_TYPE, default='renter')
    login_at = models.DateTimeField()

    def save(self, *args, **kwargs) -> None:
        self.login_at = datetime.datetime.now(tz=timezone.utc)
        return super().save(*args, **kwargs)