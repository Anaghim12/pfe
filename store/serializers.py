from django.db import transaction
from rest_framework import serializers
#pour convertir en decimal a number
from decimal import Decimal
from .models import Cart, CartItem, Collection, Order, OrderItem, Product ,Customer, ProductImage, Review, Slide
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
            raise serializers.ValidationError('no cart with the given ID was found.')
        # if the cart_id given is empty (no reason to create an empty order)
        if CartItem.objects.filter(cart_id=cart_id).count()==0:
            raise serializers.ValidationError('The cart is empty.')
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
            # we creating a list of order_items
            order_items =[
                OrderItem(
                    order=order,
                    product = item.product,
                    unit_price=item.product.unit_price,
                    quantity= item.quantity
                )for item in cart_items
            ]
            # we are saving all of our orderItems all in once thanks to bluk
            OrderItem.objects.bulk_create(order_items)
            # delete the shopping cart
            Cart.objects.filter(pk=self._validated_data['cart_id']).delete()
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
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
    class Meta:
        model = Review
        fields =['id','date','name','description']


