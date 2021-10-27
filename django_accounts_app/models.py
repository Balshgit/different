from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class CustomUser(AbstractUser):

    mobile = models.CharField(max_length=15, null=True, blank=True, unique=True,
                              help_text='Users mobile phone')
    verification_code = models.CharField(max_length=10, unique=True, null=True, blank=True,
                                         help_text='Verification code for bot account')
    user_created = models.DateField(editable=False, auto_now_add=True, verbose_name='User created',
                                    help_text='Date when user has been created')
    email = models.EmailField(max_length=30, unique=True, blank=False, null=True, help_text='User email')
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()

    def __str__(self):
        return self.username
