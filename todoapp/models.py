from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import date
# Create your models here.

class TodoModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField() 
    created_date = models.DateField()


    def __str__(self):
        return self.title
