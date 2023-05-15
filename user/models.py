from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    email = models.EmailField(
        _('email address'),
        unique=True
    )
    username = models.CharField(max_length=250, default='user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
