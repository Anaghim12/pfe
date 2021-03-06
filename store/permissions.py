import pdb
from rest_framework import permissions
from store.models import Order, Store
from rest_framework import serializers
class IsAminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
# permission accée que pour les vendeurs
class VendeurOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.type.role=='2')
class VendeurOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ('HEAD','OPTIONS'):
            return True
        # raise serializers.ValidationError('V')
        return bool((request.user and request.user.type.role=='2')or(request.user.is_superuser==True))
# permission accée que pour les vendeurs qui possédent ce store
class VendeurOwnerStoreOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return (obj.store_id == request.user.id and request.user.type.id ==4)
        # return  bool( obj.user_id==request.user.id)
# si le client ne posséde pas de profil pour (afin de savoir ces données =>d'ou on peut livrer ce produit à ce client )
# Rq: on veux un profil remplit d'une façon manuelle car un profil vide est crée d'une façon automatique
class ClientOwnAProfile(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        # return bool(request.user.type.role=='1' and request.user.customer.street != 'no street')
        return bool(request.user.type_id==1 and request.user.customer.street != 'no street')
class Client(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        # return bool(request.user.type.role=='1' and request.user.customer.street != 'no street')
        return bool(request.user.type_id==1 )
class ClientOwnAnOrder(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        # return bool(request.user.type.role=='1' and request.user.customer.street != 'no street')
        
        user=request.user.id
        return bool( request.user.type_id==1 and Order.objects.filter(customer=user).exists() )
