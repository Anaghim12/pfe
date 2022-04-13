from djoser.serializers import UserSerializer as BaseUserSerializer , UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers

#we want to add some fields in the built in serializer when creating a user
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):#inherite everything from the base class this is affect the endpoint:auth/auth (post),
        type:serializers.CharField()
        fields = ['id','first_name','last_name','username','email','password','type']
#we want to add some fields (lil djoser serializer lil current user) aprés avoir accéder à current user
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id','first_name','last_name','username','email']