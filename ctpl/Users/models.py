from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name =None
    last_name = None
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)



    