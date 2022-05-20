from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import User
from django.shortcuts import render
# from .serializers import UserCreateSerializer
# Create your views here.
#test front ***********this is for register
@api_view(['POST'])
def EmailExists(request):
    try:
        User.objects.get(email=request.data['email'])
        return Response({'Message':'Cet email exist'},status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'Message':"Cet email n' existe pas !!"},status=status.HTTP_200_OK)
@api_view(['POST'])
def LogInValidation(request):
    if User.objects.get(email=request.data['email']):
        user=User.objects.get(email=request.data['email'])
        if user.is_active==False:
            return Response({'Message':"Votre compte n'est encore activé!!!"},status=status.HTTP_400_BAD_REQUEST)
    return Response({'Message':"IL faut s'assurer de vos informations entrées!!"},status=status.HTTP_400_BAD_REQUEST)