from audioop import reverse
from dataclasses import fields
from django.db import transaction
from rest_framework import serializers
#pour convertir en decimal a number
from decimal import Decimal
from .models import *
from .signals import order_created
from rest_framework.reverse import reverse
#Aprodserializer
class AprodSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        product_id =self.context['product_id']
        return Aprod.objects.create(product_id =product_id , **validated_data)
    class Meta:
        model = Aprod
        fields =['id','inventory','color','size']
#storeimageserializer
class StoreImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        store_id =self.context['store_id']
        return StoreImage.objects.create(store_id =store_id , **validated_data)
    class Meta:
        model = StoreImage
        fields =['id','store_image']

class ProductImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        product_id =self.context['product_id']
        return ProductImage.objects.create(product_id =product_id , **validated_data)
    class Meta:
        model = ProductImage
        fields =['id','image']
class SimpleReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields =['date','description','name']

#productSerializer
class ProductSerializer(serializers.ModelSerializer):
    images =ProductImageSerializer(many=True, read_only=True) 
    # url = serializers.SerializerMethodField(read_only=True)
    # def get_url(self,obj):
    #     request= self.context.get('request')
    #     if request is None:
    #         return None
    #     return reverse("product_list",kwargs={"pk":obj.pk}, request = request)
    def create(self, validated_data):
        request =self.context.get('request')
        store_id=request.user.store.user_id
        return Product.objects.create(store_id =store_id , **validated_data)
    reviews = SimpleReviewSerializer(many=True, read_only=True)
    class Meta:
        model =Product
        fields =['id','title','get_absolute_url','unit_price','store_price','promotion','characteristic','collection','material','sub_collection','price_with_tax','inventory','description','images','reviews']

    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # collection = serializers.HyperlinkedRelatedField (
    #     queryset = Collection.objects.all(),
    #     view_name= 'collection_detail'
    # )
    def calculate_tax(self,product:Product):
          return product.unit_price * Decimal(1.1)
    
class CustomerSerializer(serializers.ModelSerializer):
    # user_id = serializers.IntegerField()

    class Meta:
        model = Customer
        # fields = ['id', 'user_id', 'phone1','phone2', 'birth_date','zipcode','street','city']  
        fields = ['user', 'phone1','phone2', 'birth_date','zipcode','street','city']  
class UpdateCustomerSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = self.context['user']
        return Customer.objects.create(user=user,**validated_data)

    class Meta:
        model = Customer

        fields = ['phone1','phone2', 'birth_date','zipcode','street','city']  
#'user_id 'is created dynamically at run time
#product simple object (pour minimiser les fields)
    
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Product
        fields =['id','title','unit_price']
#cartitem
class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only = True)
    total_price =serializers.SerializerMethodField()

    def get_total_price(self,cart_item:CartItem):
        return cart_item.quantity * cart_item.product.unit_price
    class Meta:
        model = CartItem
        fields =['id','product','quantity','total_price']
#prodWishListItem

class AddProdWishListSerializer(serializers.ModelSerializer):
    user_id =serializers.IntegerField()# capture current user
    product_id =serializers.IntegerField()#capture de url
    class Meta:
        model =CartItem
        fields = ['id','product_id','note','user_id']

#cartitem(Create a new item)#on le définit car on a besoin pour ce faire : product_id à ajouter
class AddCartItemSerializer(serializers.ModelSerializer):
    # we define this because it is dynamically created ( it is created a run time)
    product_id =serializers.IntegerField()

    class Meta:
        model =CartItem
        fields = ['id','product_id','quantity','cart']

# cart 
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True)
    items = CartItemSerializer(many= True,read_only = True)
    total_price = serializers.SerializerMethodField()
    def get_total_price(self,cart):
        return sum([item.quantity*item.product.unit_price for item in cart.items.all()])
    class Meta:
        model = Cart
        fields =['id','items','total_price']
class prodItemWishListSerializer(serializers.ModelSerializer):
    products  = SimpleProductSerializer()
    class Meta:
        model = ProdItemWishList
        fields =['user','id','products','note']
class ProdWishListSerializer(serializers.ModelSerializer):
    prod_item_wish = prodItemWishListSerializer(many=True,read_only = True)
    class Meta:
        model = ProdWishList
        fields =['user','prod_item_wish']
class AddprodItemWishListSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = self.context['user']
        return ProdItemWishList.objects.create(user=user,**validated_data)
    products_id =serializers.IntegerField()
    class Meta:
        model = ProdItemWishList
        fields = ['products_id','note']
#store wish list
class SimpleStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model= Store
        fields =['user','store_name','description']
class StoreItemWishListSerializer(serializers.ModelSerializer):
    store  = SimpleStoreSerializer()
    class Meta:
        model = StoreItemWishList
        fields =['user','id','store','note']
class StoreWishListSerializer(serializers.ModelSerializer):
    store_item_wish = StoreItemWishListSerializer(many=True,read_only = True)
    class Meta:
        model = StoreWishList
        fields =['user','store_item_wish']
class AddStoreItemWishListSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = self.context['user']
        return StoreItemWishList.objects.create(user=user,**validated_data)
    store_id =serializers.IntegerField()
    class Meta:
        model = StoreItemWishList
        fields = ['store_id','note']
#store
    # def create(self, validated_data):
    #     user = self.context['user']
    #     return StoreReview.objects.create(user=user,**validated_data)
class SimpleStoreReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreReview
        fields =['date','description','name']

class StoreSerializer(serializers.ModelSerializer):
    # user: serializers.IntegerField()
    StoreImage = StoreImageSerializer(many=True,read_only = True)
    reviews=SimpleStoreReviewSerializer(many=True,read_only = True)
    class Meta:
        model = Store
        # fields =['id','user','store_name','description','brand']
        fields =['user','store_name','description','brand','StoreImage','reviews']
class UpdateStoreSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = self.context['user']
        return Store.objects.create(user=user,**validated_data)
    class Meta:
        model = Store
        # fields =['id','user','store_name','description','brand']
        fields =['store_name','description','brand']
#orderitemSerializer
class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields =['id','product','unit_price','quantity']
#orderSerializer
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many = True,read_only=True)
    class Meta:
        model = Order
        fields = ['id','customer','placed_at','payment_status','items']
class CreateOrderSerializer(serializers.Serializer):
    cart_id =serializers.UUIDField()
    # to validate the data we receive (cart_id)
    def validate_cart_id(self,cart_id):
        # if the cart_id given is not found in DB
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('Cette carte id est introuvable!!')
        # if the cart_id given is empty (no reason to create an empty order)
        if CartItem.objects.filter(cart_id=cart_id).count()==0:
            raise serializers.ValidationError('La carte est vide!!')
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            #print (self.validated_data['cart_id'])
            #print (self.context['user_id'])
            # to get the current customer
            (customer,created) = Customer.objects.get_or_create(user_id=self.context['user_id'])
            # to create a new order for this customer
            order = Order.objects.create(customer=customer)
            # to get all the cart items of the cart_id 
            cart_items = CartItem.objects.filter(cart_id=self.validated_data['cart_id'])
            #print(customer)# anaghim ben souissi
            #print(customer.order_count)#none
            order_count=customer.order_count +1
            #print(order_count)
            # print(order_count)
            if order_count<500:
                membership="B"
            elif order_count>500:
                membership="S"
            else:
                membership="G"
            
            Customer.objects.filter(user=customer.user).update(order_count=order_count,membership=membership)
            #print(customer.order_count)
            # customer.update(membership=membership)
            # we creating a list of order_items
            order_items =[
                OrderItem(
                    order=order,
                    product = item.product,
                    unit_price=item.product.unit_price,
                    quantity= item.quantity
                )for item in cart_items
            ]
            print(order_items)
            print(order_items[0].product.store)#anaghim 's store
            print(order_items[0].product.store.user)# anaghimbensouissi@gmail.com
            for item in order_items:
                store=item.product.store
                order_count= store.order_count + 1
                if order_count<5000:
                    membership = "B"
                elif order_count<200000:
                    membership ="S"
                else: membership="G"
                Store.objects.filter(user= store.user).update(order_count=order_count,membership=membership)

            # we are saving all of our orderItems all in once thanks to bluk
            OrderItem.objects.bulk_create(order_items)
            # delete the shopping cart
            Cart.objects.filter(pk=self.validated_data['cart_id']).delete()
            order_created.send_robust(self.__class__,order=order)
            # we return an object (order) from this serializer
            return order
class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']
class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields =['id','slide_image']



#ReviewSerializer
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields =['id','date','description','name','product']

class CreateReviewSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        name = self.context['name']
        product_id =self.context['product_id']
        return Review.objects.create(product_id =product_id,name=name,**validated_data)
    class Meta:
        model = Review
        fields =['id','date','description']
#ReviewSerializer
class StoreReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreReview
        fields =['id','date','description','name','store']

class CreateStoreReviewSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        name = self.context['name']
        store_id =self.context['store_id']
        return StoreReview.objects.create(store_id =store_id,name=name,**validated_data)
    class Meta:
        model = StoreReview
        fields =['id','date','description']

#collectionSerializer


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model =Collection
        fields =['id','title','is_active','SubCollections']
#subcategoriesSerializer
class SubCollectionSerializer(serializers.ModelSerializer):
    products =SimpleProductSerializer(many=True, read_only=True) 
    class Meta:
        model = SubCollection
        fields =['id','title','products']
class ListSubCollectionSerializer(serializers.ModelSerializer):
    products =SimpleProductSerializer(many=True, read_only=True) 
    class Meta:
        model =SubCollection
        fields =['id','title','products']

class ListCollectionSerializer(serializers.ModelSerializer):
    SubCollections =ListSubCollectionSerializer(many=True, read_only=True) 
    class Meta:
        model =Collection
        fields =['id','title','SubCollections']

# class ProductWishListSerializer(serializers.ModelSerializer):
#     def create(self, validated_data):
#         user=self.context['user']
#         return ProductImage.objects.create(user=user , **validated_data)
#     class Meta:
#         model = ProdItemWishList
#         fields =['id','products','note']

# class StoreWishListSerializer(serializers.ModelSerializer):
#     def create(self, validated_data):
#         user=self.context['user']
#         return ProductImage.objects.create(user=user , **validated_data)
#     class Meta:
#         model = StoreWishList
#         fields =['id','stores','note']