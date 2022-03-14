from dataclasses import field, fields
from pyexpat import model
from rest_framework import serializers
#pour convertir en decimal a number
from decimal import Decimal
from store.models import Cart, CartItem, Collection, Product ,Customer, ProductImage, Review
#collectionSerializer
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model =Collection
        fields =['id','title']
        # fields =['id','title','products_count']

        products_count = serializers.IntegerField(read_only=True)

class ProductImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        product_id =self.context['product_id']
        return ProductImage.objects.create(product_id =product_id , **validated_data)
    class Meta:
        model = ProductImage
        fields =['id','image']
#productSerializer
class ProductSerializer(serializers.ModelSerializer):
    images =ProductImageSerializer(many=True, read_only=True) 
    class Meta:
        model =Product
        fields =['id','title','unit_price','collection','price_with_tax','inventory','slug','description','images']
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
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']  
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
#cartitem(Create a new item)#on le définit car on a besoin pour ce faire : product_id à ajouter
class AddCartItemSerializer(serializers.ModelSerializer):
    # we define this because it is dynamically created
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


#ReviewSerializer
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields =['id','date','name','description','product']

