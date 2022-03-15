from itertools import product
from django.db.models.aggregates import Count

#fro rest_framework
from rest_framework.response import Response
from rest_framework.decorators import api_view

from store.filters import ProductFilter
from store.permissions import IsAminOrReadOnly
from .models import *
from .serializers import *
from rest_framework import status
from django.shortcuts import get_object_or_404
# this is for using class-based views

from rest_framework import generics
# to get the current user profile
from rest_framework.decorators import  permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
#this is for filtering
from django_filters.rest_framework import DjangoFilterBackend

#searching
from rest_framework.filters import SearchFilter , OrderingFilter
#this is for pagination
from rest_framework.pagination import PageNumberPagination
# this for cart 
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
#Manage Client Reviews to the product
class ReviewCreateViewSet(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
class ReviewListViewSet(generics.ListAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

#Manage Client Reviews to the stores

#Manage slide
class SlideCreateViewSet(generics.CreateAPIView):
    serializer_class = SlideSerializer
    permission_classes = [IsAdminUser]
    queryset = Slide.objects.all()

class SlideListViewSet(generics.ListAPIView):
    serializer_class = SlideSerializer
    permission_classes = [IsAdminUser]
    queryset = Slide.objects.all()

class SlideUpdateViewSet(generics.UpdateAPIView):
    serializer_class = SlideSerializer
    permission_classes = [IsAdminUser]
    queryset = Slide.objects.all()

class SlideDestroyViewSet(generics.DestroyAPIView):
    serializer_class = SlideSerializer
    permission_classes = [IsAdminUser]
    queryset = Slide.objects.all()

#Manage Orders
class OrderCreateViewSet(generics.CreateAPIView):
    serializer_class = CreateOrderSerializer
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        # we use the first serializer (CreateOrderSerializer) to do the first part of the job (voir serializer)
        serializer = CreateOrderSerializer(
            data=request.data,
            context={'user_id':self.request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        # we caputre in here the result of the first serializer (voir serializer)
        order = serializer.save()
        # we use in here the second serializer pour afficher the order object created et non pas cart_id (qui existe fil CreateOrderSerializer)
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class OrderListViewSet(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        # s'il s'agit d'un admin il va voir tous les orders
        if user.is_staff:
            return Order.objects.all()
        #s'il est authentifié il va voir que ces ordres
        customer_id = Customer.objects.only('id').get(user_id = user)
        return Order.objects.filter(customer_id=customer_id)

class OrderRetreiveViewSet(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        # s'il s'agit d'un admin il va voir tous les orders
        if user.is_staff:
            return Order.objects.all()
        #s'il est authentifié il va voir que ces ordres
        customer_id = Customer.objects.only('id').get(user_id = user)
        return Order.objects.filter(customer_id=customer_id)
class OrderDestroyViewSet(generics.DestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
class OrderUpdateViewSet(generics.UpdateAPIView):
    serializer_class = UpdateOrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
#Manage cartitem
class ItemCartUpdateViewSet(generics.UpdateAPIView):
    serializer_class = CartItemSerializer
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')

class ItemCartDestroyViewSet(generics.DestroyAPIView):
    serializer_class = CartItemSerializer
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')

class ItemCartRetreiveViewSet(generics.RetrieveAPIView):
    serializer_class = CartItemSerializer
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')
class ItemCartListViewSet(generics.ListAPIView):
    serializer_class = CartItemSerializer
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')

class ItemCartCreateViewSet(generics.CreateAPIView):
    serializer_class = AddCartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])
    
#Manage Cart
class CartCreateViewSet(generics.CreateAPIView):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer
class CartRetrieveViewSet(generics.RetrieveAPIView):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer
class CartDestroyViewSet(generics.DestroyAPIView):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer
#Manage Product Images
class ProductImageCreateViewSet(generics.CreateAPIView):
    
    serializer_class = ProductImageSerializer
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
    def get_queryset(self):
        return ProductImage.objects.filter(product_id= self.kwargs['product_pk'])# to bring from the url the id of the product

class ProductImageUpdateViewSet(generics.UpdateAPIView):
    
    serializer_class = ProductImageSerializer
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
    def get_queryset(self):
        return ProductImage.objects.filter(product_id= self.kwargs['product_pk'])

class ProductImageRetrieveViewSet(generics.RetrieveAPIView):
    
    serializer_class = ProductImageSerializer
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
    def get_queryset(self):
        return ProductImage.objects.filter(product_id= self.kwargs['product_pk'])

class ProductImageListViewSet(generics.ListAPIView):
    
    serializer_class = ProductImageSerializer
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
    def get_queryset(self):
        return ProductImage.objects.filter(product_id= self.kwargs['product_pk'])
class ProductImageDestroyViewSet(generics.DestroyAPIView):
    
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        return ProductImage.objects.filter(product_id= self.kwargs['product_pk'])
#auth
class CustomerCreateViewSet(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
class CustomerRetreiveUpdateViewSet(generics.RetrieveUpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
#auth to get current customer(ili 3amil log in )

#Product CRUD
class ProductCreate(generics.CreateAPIView):
    queryset=Product.objects.all()
    serializer_class =ProductSerializer
    permission_classes =[IsAminOrReadOnly]

class ProductList(generics.ListAPIView):
    queryset=Product.objects.prefetch_related('images').all()
    serializer_class =ProductSerializer
    filter_backends  =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title','description']
    ordering_fields =['unit_price','last_update']
    pagination_class = PageNumberPagination
class ProductRetreive(generics.RetrieveAPIView):
    queryset=Product.objects.prefetch_related('images').all()
    serializer_class =ProductSerializer
class ProductUpdate(generics.UpdateAPIView):
    queryset=Product.objects.all()
    serializer_class =ProductSerializer
    permission_classes =[IsAminOrReadOnly]

class ProductDestroy(generics.DestroyAPIView):
    queryset=Product.objects.all()
    #permission_classes =[IsAminOrReadOnly]
    serializer_class =ProductSerializer
    def delete(self,request,pk):
        product = get_object_or_404(Product, pk=pk) # to get the product
        if product.orderitems.count() > 0:# par défaut orderitem_set # if there is any order items associated with this product (sinon kan manhotich heda el code tjini erreur 5atir el product is Protected fil orderItem class fil model)
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#Category CRUD
class CollectionCreate(generics.CreateAPIView):
    queryset=Collection.objects.all()
    serializer_class =CollectionSerializer
    permission_classes =[IsAminOrReadOnly]
class CollectionList(generics.ListAPIView):
    queryset=Collection.objects.all()
    serializer_class =CollectionSerializer
class CollectionRetreive(generics.RetrieveAPIView):
    queryset=Collection.objects.all()
    serializer_class =CollectionSerializer
    permission_classes =[IsAminOrReadOnly]
class CollectionUpdate(generics.UpdateAPIView):
    queryset=Collection.objects.all()
    serializer_class =CollectionSerializer
    permission_classes =[IsAminOrReadOnly]
class CollectionDestroy(generics.DestroyAPIView):
    def get_queryset(self):
        return Collection.objects.all()
    def get_serializer_class(self):
        return CollectionSerializer
    def delete(self,request,pk):
        product = get_object_or_404(Product, pk=pk) # to get the product
        if product.orderitems.count() > 0:# par défaut orderitem_set # if there is any order items associated with this product (sinon kan manhotich heda el code tjini erreur 5atir el product is Protected fil orderItem class fil model)
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#Reviews

###############collections
#get all collections + create a collection

# M1: implémentation with function based views
# get all products
# @api_view(['GET','POST'])
# def product_list(request):
#     if request.method =='GET':
#         queryset= Product.objects.all()
#         serializer= ProductSerializer(queryset, many =True, context={'request':request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data) #deserialize de data existed in the body
#         serializer.is_valid(raise_exception=True) # s'assurer qu'elle est valide le paramère passer c'est pour ne pas faire bloc: if else
#         print(serializer.validated_data)
#         serializer.save() #save the object in the database
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#Auth CRUD
class CustomerCreate(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes=[IsAdminUser]
class CustomerRetrieve(generics.RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes=[IsAdminUser]
class CustomerList(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes=[IsAdminUser]
class CustomerUpdate(generics.UpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes=[IsAdminUser]
#only authanticated customer can get or update their profile 
@api_view(['Get','PUT'])
@permission_classes([IsAuthenticated])
def CustomerCurrent(request):
    customer=Customer.objects.get(user_id=request.user.id)
    if request.method == 'GET':
        serializer=CustomerSerializer(customer)
        return Response(serializer.data)
    elif request.method =='PUT':
        serializer = CustomerSerializer(customer,data =request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

#detail prodcuts
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id) # to get the product
    if request.method == 'GET':
        serializer = ProductSerializer(product) # to serialize the data
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data) # desirialize the data comming from the user bich ywali object then call the save qui va réaliser el update method car il existe 2 arguments 
        serializer.is_valid(raise_exception=True) # valider data selon mon model + serializer (if there is a custom validation)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if product.orderitems.count() > 0:# par défaut orderitem_set # if there is any order items associated with this product (sinon kan manhotich heda el code tjini erreur 5atir el product is Protected fil orderItem class fil model)
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

###############collections
#get all collections + create a collection
@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(products_count=Count('products')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
#detail collection
@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk) # get the collection and annotate them with the numberof product in each collection
    if request.method == 'GET':
        serializer = CollectionSerializer(collection) # to serialize the data
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data) 
        serializer.is_valid(raise_exception=True) 
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if collection.products.count() > 0: # if the collection have any product 5atir el collection is Protected fil product class fil model)
            return Response({'error': 'Collection cannot be deleted because it includes one more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
