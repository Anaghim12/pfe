from django.urls import path
from . import views

urlpatterns =[
    path('exist_email/',views.EmailExists),
    path('exist_email/',views.LogInValidation),




]