from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Type(models.Model):
    role = models.CharField(max_length=255)
    def __str__(self):
        return self.role

class User(AbstractUser):
    email=models.EmailField(unique=True)
    type = models.ForeignKey(Type,on_delete=models.CASCADE,default=1)
