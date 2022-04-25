from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models.aggregates import Count
from django.db.models import Q 
from .filters import ProductFilter
from .pagination import DefaultPagination
from .permissions import *
from .models import *
from .serializers import *
from .pagination import *
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
#manage Aprod
class AprodCreateViewSet(generics.CreateAPIView):
    permission_classes = [VendeurOrAdmin]
    serializer_class = AprodSerializer
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
    def get_queryset(self):
        return Aprod.objects.filter(product_id= self.kwargs['product_pk'])
class AprodUpdateViewSet(generics.UpdateAPIView):
    permission_classes = [VendeurOrAdmin]
    serializer_class = AprodSerializer
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
    def get_queryset(self):
        return Aprod.objects.filter(product_id= self.kwargs['product_pk'])
class AprodRetreiveViewSet(generics.RetrieveAPIView):
    permission_classes = [VendeurOrAdmin]
    serializer_class = AprodSerializer
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
    def get_queryset(self):
        return Aprod.objects.filter(product_id= self.kwargs['product_pk'])
class AprodListViewSet(generics.ListAPIView):
    permission_classes = [VendeurOrAdmin]
    serializer_class = AprodSerializer
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
    def get_queryset(self):
        return Aprod.objects.filter(product_id= self.kwargs['product_pk'])
        
class AprodDestroyViewSet(generics.DestroyAPIView):
    permission_classes = [VendeurOrAdmin]
    serializer_class = AprodSerializer
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
    def get_queryset(self):
        return Aprod.objects.filter(product_id= self.kwargs['product_pk'])       
#Manage store Images
class StoreImageCreateViewSet(generics.CreateAPIView):
    permission_classes = [VendeurOrReadOnly]
    serializer_class = StoreImageSerializer
    def get_serializer_context(self):
        return {'store_id':self.kwargs['store_pk']}
    def get_queryset(self):
        return StoreImage.objects.filter(store_id= self.kwargs['store_pk'])# to bring from the url the id of the product

class StoreImageUpdateViewSet(generics.UpdateAPIView):
    permission_classes = [VendeurOwnerStoreOrReadOnly]
    serializer_class = StoreImageSerializer
    def get_serializer_context(self):
        return {'store_id':self.kwargs['store_pk']}
    def get_queryset(self):
        return StoreImage.objects.filter(store_id= self.kwargs['store_pk'])

class StoreImageRetrieveViewSet(generics.RetrieveAPIView):
    
    serializer_class = StoreImageSerializer
    def get_serializer_context(self):
        return {'store_id':self.kwargs['store_pk']}
    def get_queryset(self):
        return StoreImage.objects.filter(store_id= self.kwargs['store_pk'])

class StoreImageListViewSet(generics.ListAPIView):
    
    serializer_class = StoreImageSerializer
    def get_serializer_context(self):
        return {'store_id':self.kwargs['store_pk']}
    def get_queryset(self):
        return StoreImage.objects.filter(store_id= self.kwargs['store_pk'])
class StoreImageDestroyViewSet(generics.DestroyAPIView):
    permission_classes = [VendeurOwnerStoreOrReadOnly]
    serializer_class = StoreImageSerializer

    def get_queryset(self):
        return StoreImage.objects.filter(store_id= self.kwargs['store_pk'])

#manage store
class StoreCreate(generics.CreateAPIView):
    queryset=Store.objects.all()
    serializer_class =StoreSerializer
    permission_classes = [IsAdminUser,VendeurOrReadOnly]

class StoreList(generics.ListAPIView):
    queryset=Store.objects.prefetch_related('StoreImage').all()
    serializer_class =StoreSerializer
    


    pagination_class =DefaultPagination
class StoreRetreive(generics.RetrieveAPIView):
    queryset=Store.objects.prefetch_related('StoreImage').all()
    serializer_class =StoreSerializer
  

class StoreUpdate(generics.UpdateAPIView):
    queryset=Store.objects.all()
    serializer_class =UpdateStoreSerializer
    # permission_classes = [IsAdminUser]
    def get_serializer_context(self):
        return {'user':self.request.user}

class StoreDestroy(generics.DestroyAPIView):
    queryset=Store.objects.all()
    serializer_class =StoreSerializer
    permission_classes = [IsAdminUser,VendeurOwnerStoreOrReadOnly]

#manage storewishList
class StoreWishListListViewSet(generics.ListAPIView):
    serializer_class = StoreWishListSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user= self.request.user
        if user.is_staff:
            return StoreWishList.objects.prefetch_related('store_item_wish__store').all()
        return StoreWishList.objects.prefetch_related('store_item_wish__store').filter(user=user)
#normalement n'est important celle ci (pas la peine de l'implémenter)
class StoreWishListRetreiveViewSet(generics.RetrieveAPIView):
    serializer_class = StoreWishListSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user= self.request.user
        if user.is_staff:
            return StoreWishList.objects.prefetch_related('store_item_wish__store').all()
        return StoreWishList.objects.prefetch_related('store_item_wish__store').filter(user=user)

class StoreWishListDestroyViewSet(generics.DestroyAPIView):
    serializer_class = StoreWishListSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user= self.request.user
        if user.is_staff:
            return StoreWishList.objects.all()
        return StoreWishList.objects.filter(user=user)

class StoreWishListCreateViewSet(generics.CreateAPIView):
    serializer_class = StoreWishListSerializer
    permission_classes = [IsAuthenticated]
    queryset = StoreWishList.objects.all()


#manage storeItemWishList
class StoreItemWishListListViewSet(generics.ListAPIView):
    serializer_class = StoreItemWishListSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user= self.request.user
        if user.is_staff:
            return StoreItemWishList.objects.all()
        return StoreItemWishList.objects.filter(user=user)

class StoreItemWishListCreateViewSet(generics.CreateAPIView):
    serializer_class = AddStoreItemWishListSerializer
    permission_classes = [IsAuthenticated]
    def get_serializer_context(self):
        return {'user':self.request.user}
    queryset= StoreItemWishList.objects.all()

class StoreItemWishListDestroyViewSet(generics.DestroyAPIView):
    serializer_class = StoreItemWishListSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user= self.request.user
        if user.is_staff:
            return StoreItemWishList.objects.all()
        return StoreItemWishList.objects.filter(user=user)
class StoreItemWishListUpdateViewSet(generics.UpdateAPIView):
    serializer_class = AddStoreItemWishListSerializer
    permission_classes = [IsAuthenticated]
    def get_serializer_context(self):
        return {'user':self.request.user}
    def get_queryset(self):
        user= self.request.user
        if user.is_staff:
            return StoreItemWishList.objects.all()
        return StoreItemWishList.objects.filter(user=user)
#manage prodItemWishList
class ProdItemWishListListViewSet(generics.ListAPIView):
    serializer_class = prodItemWishListSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user= self.request.user
        if user.is_staff:
            return ProdItemWishList.objects.all()
        return ProdItemWishList.objects.filter(user=user)

class ProdItemWishListCreateViewSet(generics.CreateAPIView):
    serializer_class = AddprodItemWishListSerializer
    permission_classes = [IsAuthenticated]
    # def get_serializer_context(self):
    #     return {'user_id':self.request.user}
    queryset= ProdItemWishList.objects.all()

class ProdItemWishListDestroyViewSet(generics.DestroyAPIView):
    serializer_class = prodItemWishListSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user= self.request.user
        if user.is_staff:
            return ProdItemWishList.objects.all()
        return ProdItemWishList.objects.filter(user=user)
class ProdItemWishListUpdateViewSet(generics.UpdateAPIView):
    serializer_class = AddprodItemWishListSerializer
    permission_classes = [IsAuthenticated]
    def get_serializer_context(self):
        return {'user':self.request.user}
    def get_queryset(self):
        user= self.request.user
        if user.is_staff:
            return ProdItemWishList.objects.all()
        return ProdItemWishList.objects.filter(user=user)
#manage prodwishList
class ProdWishListListViewSet(generics.ListAPIView):
    serializer_class = ProdWishListSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user= self.request.user
        if user.is_staff:
            return ProdWishList.objects.prefetch_related('prod_item_wish__products').all()
        return ProdWishList.objects.prefetch_related('prod_item_wish__products').filter(user=user)

class ProdWishListRetreiveViewSet(generics.RetrieveAPIView):
    serializer_class = ProdWishListSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user= self.request.user
        if user.is_staff:
            return ProdWishList.objects.prefetch_related('prod_item_wish__products').all()
        return ProdWishList.objects.prefetch_related('prod_item_wish__products').filter(user=user)

class ProdWishListDestroyViewSet(generics.DestroyAPIView):
    serializer_class = ProdWishListSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user= self.request.user
        if user.is_staff:
            return ProdWishList.objects.all()
        return ProdWishList.objects.filter(user=user)

class ProdWishListCreateViewSet(generics.CreateAPIView):
    serializer_class = ProdWishListSerializer
    permission_classes = [IsAuthenticated]

    queryset = ProdWishList.objects.all()

#manage StoreWishList
#search and filters 
class SearchProduct(generics.ListAPIView):
    serializer_class =ProductSerializer
    def get_queryset(self,*args,**kwargs):
        q= self.request.GET.get('q')
        result=Product.objects.none()
        if q is not None :
            lookup=Q(title__icontains=q)|Q(description__icontains=q)|Q(store__store_name__icontains=q)
            result= Product.objects.filter(is_active=True).filter(lookup)
        return result
#Manage Client Reviews to the product
class ReviewCreateViewSet(generics.CreateAPIView):
    serializer_class = CreateReviewSerializer
    permission_classes = [IsAuthenticated]
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk'],'name':self.request.user}
    queryset = Review.objects.all()

class ReviewListViewSet(generics.ListAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

class ReviewUpdateViewSet(generics.UpdateAPIView):
    serializer_class = CreateReviewSerializer
    permission_classes = [IsAuthenticated]
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk'],'name':self.request.user}
    
    def get_queryset(self):
        user = self.request.user
        # s'il s'agit d'un admin il va voir tous les orders
        if user.is_staff:
            return Review.objects.all()
        #s'il est authentifié il va voir que ces ordres
        return Review.objects.filter(name=user)

class ReviewDestroyViewSet(generics.DestroyAPIView):
    serializer_class = CreateReviewSerializer
    permission_classes = [IsAuthenticated]
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk'],'name':self.request.user}
    
    def get_queryset(self):
        user = self.request.user
        # s'il s'agit d'un admin il va voir tous les orders
        if user.is_staff:
            return Review.objects.all()
        #s'il est authentifié il va voir que ces ordres
        return Review.objects.filter(name=user)
#Manage Client Reviews to the stores
class StoreCreateViewSet(generics.CreateAPIView):
    serializer_class = CreateStoreReviewSerializer
    permission_classes = [IsAuthenticated]
    def get_serializer_context(self):
        return {'store_id':self.kwargs['store_pk'],'name':self.request.user}
    queryset = StoreReview.objects.all()

class StoreListViewSet(generics.ListAPIView):
    serializer_class = StoreReviewSerializer
    queryset = StoreReview.objects.all()

class StoreUpdateViewSet(generics.UpdateAPIView):
    serializer_class = CreateStoreReviewSerializer
    permission_classes = [IsAuthenticated]
    def get_serializer_context(self):
        return {'store_id':self.kwargs['store_pk'],'name':self.request.user}
    
    def get_queryset(self):
        user = self.request.user
        # s'il s'agit d'un admin il va voir tous les orders
        if user.is_staff:
            return StoreReview.objects.all()
        #s'il est authentifié il va voir que ces ordres
        return StoreReview.objects.filter(name=user)

class StoreDestroyViewSet(generics.DestroyAPIView):
    serializer_class = CreateStoreReviewSerializer
    permission_classes = [IsAuthenticated]
    def get_serializer_context(self):
        return {'store_id':self.kwargs['store_pk'],'name':self.request.user}
    
    def get_queryset(self):
        user = self.request.user
        # s'il s'agit d'un admin il va voir tous les orders
        if user.is_staff:
            return StoreReview.objects.all()
        #s'il est authentifié il va voir que ces ordres
        return StoreReview.objects.filter(name=user)
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

#manage order
class OrderCreateViewSet(generics.CreateAPIView):
    serializer_class = CreateOrderSerializer
    permission_classes = [ClientOwnAProfile]
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
    permission_classes = [ClientOwnAProfile]
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
#manage cartitem
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
    permission_classes=[VendeurOwnerStoreOrReadOnly,IsAdminUser]
    serializer_class = ProductImageSerializer
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
    def get_queryset(self):
        return ProductImage.objects.filter(product_id= self.kwargs['product_pk'])# to bring from the url the id of the product

class ProductImageUpdateViewSet(generics.UpdateAPIView):
    permission_classes=[VendeurOwnerStoreOrReadOnly,IsAdminUser]
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
    permission_classes=[VendeurOwnerStoreOrReadOnly,IsAdminUser]
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        return ProductImage.objects.filter(product_id= self.kwargs['product_pk'])    
#auth to get current customer(ili 3amil log in )

# manage product
class ProductCreate(generics.CreateAPIView):
    queryset=Product.objects.all()
    serializer_class =ProductSerializer
    # permission_classes =[VendeurOrReadOnly,IsAdminUser]
class MyProductList(generics.ListAPIView):
    serializer_class =ProductSerializer
    def get_queryset(self):
        result = Product.objects.filter(store=self.request.user.store)
        return result
    

class ProductList(generics.ListAPIView):
    queryset=Product.objects.filter(is_active=True).prefetch_related('images').all()
    serializer_class =ProductSerializer
    filter_backends  =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    # pagination_class = DefaultPagination
    #search_fields = ['title','description']
    ordering_fields =['unit_price']
    pagination_class =DefaultPagination
class ProductRetreive(generics.RetrieveAPIView):
    queryset=Product.objects.prefetch_related('images').prefetch_related('reviews').all()
    serializer_class =ProductSerializer
class ProductUpdate(generics.UpdateAPIView):
    queryset=Product.objects.all()
    serializer_class =ProductSerializer
    permission_classes =[VendeurOwnerStoreOrReadOnly,IsAdminUser]
class ProductDestroy(generics.DestroyAPIView):
    queryset=Product.objects.all()
    serializer_class =ProductSerializer
    permission_classes =[VendeurOwnerStoreOrReadOnly,IsAdminUser]

# class ProductDestroy(generics.DestroyAPIView):
#     queryset=Product.objects.all()
#     permission_classes =[VendeurOwnerStoreOrReadOnly,IsAdminUser]
#     serializer_class =ProductSerializer
#     def delete(self,request,pk):
#         product = get_object_or_404(Product, pk=pk) # to get the product
#         if product.orderitems.count() > 0:# par défaut orderitem_set # if there is any order items associated with this product (sinon kan manhotich heda el code tjini erreur 5atir el product is Protected fil orderItem class fil model)
#             return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#manage subcategory 
class SubCollectionCreate(generics.CreateAPIView):
    queryset=SubCollection.objects.all()
    serializer_class =SubCollectionSerializer
    permission_classes =[IsAminOrReadOnly]
class SubCollectionRetreive(generics.RetrieveAPIView):
    serializer_class =ListSubCollectionSerializer
    permission_classes =[IsAminOrReadOnly]
    def get_queryset(self):
        results= SubCollection.objects.filter(is_active=True)
        return results
class SubCollectionUpdate(generics.UpdateAPIView):
    queryset=Collection.objects.all()
    serializer_class =SubCollectionSerializer
    permission_classes =[IsAminOrReadOnly]
#manage category 
class CollectionCreate(generics.CreateAPIView):
    queryset=Collection.objects.all()
    serializer_class =CollectionSerializer
    permission_classes =[IsAminOrReadOnly]

class CollectionList(generics.ListAPIView):
    queryset=Collection.objects.all()
    serializer_class =ListCollectionSerializer
class CollectionRetreive(generics.RetrieveAPIView):
    queryset=Collection.objects.all()
    serializer_class =ListCollectionSerializer
    permission_classes =[IsAminOrReadOnly]
    def get_queryset(self):
        results= Collection.objects.filter(is_active=True)
        return results

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
# manage customer
class CustomerCreate(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes=[IsAdminUser]
class CustomerList(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes=[IsAdminUser]
class CustomerRetrieve(generics.RetrieveAPIView):
    serializer_class = UpdateCustomerSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        user= self.request.user
        if user.is_staff:
            return Customer.objects.all()
        return Customer.objects.all(user=user)
    def get_serializer_context(self):
        return {'user':self.request.user}
class CustomerUpdate(generics.UpdateAPIView):
    serializer_class = UpdateCustomerSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        user= self.request.user
        if user.is_staff:
            return Customer.objects.all()
        return Customer.objects.all(user=user)
    def get_serializer_context(self):
        return {'user':self.request.user}
class CustomerDestroy(generics.DestroyAPIView):
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
