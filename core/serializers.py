from djoser.serializers import UserSerializer as BaseUserSerializer , UserCreateSerializer as BaseUserCreateSerializer

#we want to add some fields in the built in serializer when creating a user
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):#inherite everything from the base class this is affect the endpoint:auth/auth (post),
        fields = ['id','username','password','email','first_name','last_name']
#we want to add some fields aprés avoir accéder à current user
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id','username','email','first_name','last_name']