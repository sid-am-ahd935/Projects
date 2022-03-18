from django.db import models

class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True # Not Creating any model instances by adding this model
        ordering = ('-created_at',)


