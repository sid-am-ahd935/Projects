from django.db import models

# Create your models here.
from authentication.models import User
from helpers.models import TrackingModel

class Todo(TrackingModel):
    title = models.CharField(max_length= 255)
    desc = models.TextField()
    is_complete = models.BooleanField(default= False)
    owner = models.ForeignKey(to= User, on_delete= models.CASCADE)

    def __str__(self):
        return self.title