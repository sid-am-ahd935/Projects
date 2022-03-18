from django.db import models
from django.apps import apps
from django.contrib.auth.hashers import make_password
from helpers.models import TrackingModel
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.contrib.auth.models import (
    PermissionsMixin,
    AbstractBaseUser,
    UserManager,
)
import jwt
from datetime import datetime, timedelta

from django.conf import settings

class MyUserManager(UserManager):


    def _create_user(self, username, email, password, **extra_fields):
        
        if not username:
            raise ValueError("The given username must be set")

        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin, TrackingModel):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length= 150,
        unique= True,
        validators= [username_validator],
        error_messages= {
            'unique':("A user with that username exists already.")
        },
    )
    email = models.EmailField(null= False, blank= False, unique= True)
    
    is_staff = models.BooleanField(default= False)

    is_active = models.BooleanField(default= True)

    email_verified = models.BooleanField(default= False)

    date_joined = models.DateTimeField(default= timezone.now)

    objects = MyUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ["username"]

    @property
    def token(self):
        token = jwt.encode(
            {
                "username" : self.username, 
                "email" : self.email, 
                "exp" : datetime.utcnow() + timedelta(hours=24),
            }, 
            settings.SECRET_KEY, 
            algorithm= "HS256",
        )

        return token
