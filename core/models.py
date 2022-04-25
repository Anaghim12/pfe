from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin,BaseUserManager
from django.conf import settings

# class UserAccountManager(BaseUserManager):
#     def create_user(self,username,email,first_name,last_name,type,password=None):
#         if not email :
#             raise ValueError('Users must have an email address')
#         email = self.normalize_email(email)
#         user = self.model(email=email,username=username,first_name=first_name,last_name=last_name,type=type)
#         user.set_password(password)
#         user.save()
#         return user

class Type(models.Model):
    #1 => client
    #2 => vendeur
    role = models.CharField(max_length=255, default='1')
    
    # ROLE_CLIENT = 'C'
    # ROLE_VENDEUR = 'V'

    # Role_CHOICES = [
    #     (ROLE_CLIENT, 'Client'),
    #     (ROLE_VENDEUR, 'Vendeur'),
    # ]
    # role = models.CharField(
    #     max_length=20, choices=Role_CHOICES, default=ROLE_CLIENT)
    def __str__(self):
        return self.role

class User(AbstractUser):
    email=models.EmailField(unique=True)
    type = models.ForeignKey(Type,on_delete=models.CASCADE,default=1)
    # objects = UserAccountManager()
    USERNAME_FIELD ='email'
    # REQUIRED_FIELDS =['username']
    REQUIRED_FIELDS =['first_name','last_name','username','type']
    def __str__(self):
        return self.email
        
