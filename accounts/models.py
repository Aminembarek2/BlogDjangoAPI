from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Token Authentication
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.



class UserManager(BaseUserManager):

    def create_superuser(self,email,username,password,**other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active',True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('SuperUser must be assigned to is_staff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('SuperUser must be assigned to is_superuser=True')
        return self.create_user(email,username,password, **other_fields)

    def create_user(self,email,username,password,**other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email,username=username,**other_fields)
        user.set_password(password)
        user.save()
        return user
        
class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(_('username'),max_length=50, unique=True)
    email = models.EmailField(_('email address'), blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    password = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()
    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password
'''''
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
'''