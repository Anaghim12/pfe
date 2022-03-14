from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Type(models.Model):
    role = models.CharField(max_length=255)
class User(AbstractUser):
    email=models.EmailField(unique=True)
    type = models.OneToOneField(Type,on_delete=models.CASCADE,default=1)