from asyncore import read
from audioop import reverse
from dataclasses import fields
import pdb
from turtle import pd, title
from django.db import transaction
from rest_framework import serializers
#pour convertir en decimal a number
from decimal import Decimal
from .models import *
from .signals import order_created 
from rest_framework.reverse import reverse
class OrderMsgSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields=['msg']
#cart avant ajouter panier
class GetColorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Aprod
        fields=['id','color']
class GetSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Aprod
        fields=['id','size']

#Demanderetourserializer
class DemandeRetourSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        request =self.context.get('request')
        user=request.user
        return DemandeRetour.objects.create(user =user , **validated_data)
    class Meta:
        model=DemandeRetour
        fields =['id','num_order','date_order','slug_produit_retour','cause','image_facture','image_produit']

#Aprodserializer
class AprodSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        product_id =self.context['product_id']
        return Aprod.objects.create(product_id =product_id , **validated_data)
    class Meta:
        model = Aprod
        fields =['id','inventory','color','size']
class UpdateAprodSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        product_id =self.context['product_id']
        return Aprod.objects.create(product_id =product_id , **validated_data)
    class Meta:
        model = Aprod
        fields =['inventory']
# class AprodSizeSerializer(serializers.ModelSerializer):
#     def create(self, validated_data):
#         product_id =self.context['product_id']
#         return Aprod.objects.create(product_id =product_id , **validated_data)
#     class Meta:
#         model = Aprod
#         fields =['id','inventory','color','size']
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
class RetreiveProductSerializer(serializers.ModelSerializer):
    images =ProductImageSerializer(many=True, read_only=True) 
    reviews = SimpleReviewSerializer(many=True, read_only=True)
    ProdVersion =GetSizeSerializer(many=True,read_only=True)
    class Meta:
        model =Product
        fields =['id','title','get_absolute_url','unit_price','price_with_promotion','promotion','collection','material','sub_collection','description','ProdVersion','images','reviews']
class ProductSerializer(serializers.ModelSerializer):
    images =ProductImageSerializer(many=True, read_only=True) 
    def create(self, validated_data):
        request =self.context.get('request')
        store_id=request.user.store.user_id
        product=Product(**validated_data)
        promotion=product.promotion
        price= product.unit_price
        print(promotion)
        if promotion != 0:
            print(price)
            reduction=(price*promotion)/100
            price_with_promotion=price-reduction
        else :
            price_with_promotion=price
        return Product.objects.create(store_id =store_id , price_with_promotion=price_with_promotion,**validated_data)
    
    reviews = SimpleReviewSerializer(many=True, read_only=True)
    class Meta:
        model =Product
        fields =['id','title','get_absolute_url','unit_price','store_price','promotion','collection','material','sub_collection','price_with_tax','description','images','reviews']

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
        fields =['id','title','unit_price','price_with_promotion']
class SimpleAprodSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='product.title',read_only=True)
    unit_price = serializers.CharField(source='product.price_with_promotion',read_only=True)
    class Meta: 
        model = Aprod
        fields =['slug','title','unit_price']
#cartitem
class CartItemUpdateSerializer(serializers.ModelSerializer):
    product = SimpleAprodSerializer(read_only = True)
    total_price =serializers.SerializerMethodField()
    def validate_quantity(self, quantity):
        item_id = self.context['item_id']
        print(item_id)
        item_obj=CartItem.objects.get(id=item_id)
        print(item_obj)
        # print(item_obj.product.inventory)
        if item_obj.product.inventory<quantity:
            raise serializers.ValidationError("Vous ne pouvez pas ajouter cette quantité !! Il n'existe que "+ str(item_obj.product.inventory) +" pièces au stock!!!")
        return quantity
    def get_total_price(self,cart_item:CartItem):
        return cart_item.quantity * cart_item.product.product.price_with_promotion
    class Meta:
        model = CartItem
        fields =['id','product','quantity','total_price']
class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleAprodSerializer(read_only = True)
    total_price =serializers.SerializerMethodField()
    def get_total_price(self,cart_item:CartItem):
        return cart_item.quantity * cart_item.product.product.price_with_promotion
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
        return sum([item.quantity*item.product.product.price_with_promotion for item in cart.items.all()])
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
        return ProdItemWishList.objects.create(user_id=user,**validated_data)
    def validate_products_id(self, products_id):
        user = self.context['user']
        user_id=user
        queryset_prod_item=ProdItemWishList.objects.filter(user_id=user_id)
        for item in queryset_prod_item:
            if item.products_id == products_id:
                raise serializers.ValidationError("Ce produit existe déja dans votre liste de souhaits de produit!!")
        return products_id
    products_id =serializers.IntegerField()
    class Meta:
        model = ProdItemWishList
        fields = ['products_id','note']
class UpdateprodItemWishListSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = self.context['user']
        return ProdItemWishList.objects.create(user_id=user,**validated_data)
    products_id =serializers.IntegerField()
    class Meta:
        model = ProdItemWishList
        fields = ['products_id','note']
#store wish list
class SimpleStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model= Store
        fields =['user','store_name']
class StoreItemWishListSerializer(serializers.ModelSerializer):
    store  = SimpleStoreSerializer()
    class Meta:
        model = StoreItemWishList
        fields =['id','store','note']
class StoreWishListSerializer(serializers.ModelSerializer):
    store_item_wish = StoreItemWishListSerializer(many=True,read_only = True)
    class Meta:
        model = StoreWishList
        fields =['user','store_item_wish']
class AddStoreItemWishListSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = self.context['user']
        return StoreItemWishList.objects.create(user_id=user,**validated_data)
    def validate_store_id(self, store_id):
        user = self.context['user']
        user_id=user
        queryset_store_item=StoreItemWishList.objects.filter(user_id=user_id)
        for item in queryset_store_item:
            if item.store_id == store_id:
                raise serializers.ValidationError("Cette magasin existe déja dans votre liste de souhaits de magasin!!")
        return store_id
    store_id =serializers.IntegerField()
    class Meta:
        model = StoreItemWishList
        fields = ['store_id','note']
class UpdateStoreItemWishListSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = self.context['user']
        return StoreItemWishList.objects.create(user_id=user,**validated_data)
    store_id =serializers.IntegerField()
    class Meta:
        model = StoreItemWishList
        fields = ['store_id','note']

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
    product = SimpleAprodSerializer()
    class Meta:
        model = OrderItem
        fields =['id','product','unit_price','quantity']
# class GetSubSerializer(serializers.ModelSerializer):

#orderSerializer
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many = True,read_only=True)
    total_price = serializers.SerializerMethodField()
    total_price_for_secial_clients = serializers.SerializerMethodField()
    def get_total_price(self,instance):
        return sum([item.quantity*item.product.product.price_with_promotion for item in instance.items.all()])
    def get_total_price_for_secial_clients(self,instance):
        somme= sum([item.quantity*item.product.product.price_with_promotion for item in instance.items.all()])
        membership=instance.customer.membership
        reduction=0
        print(membership)
        if membership == "S":
            reduction= (somme*5)/100
        elif membership == "G":
            reduction= (somme*10)/100
        somme=somme-reduction
        return somme
    class Meta:
        model = Order
        fields = ['id','customer','placed_at','payment_status','items','total_price','total_price_for_secial_clients']
class CreateOrderSerializer(serializers.Serializer):
    cart_id =serializers.UUIDField()
    msg=serializers.CharField(read_only=True)
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
                # qty management
            msg="aucune"
            for item in cart_items:
                product=item.product
                # if product.inventory < item.quantity:
                #     msg="Désolé,il existe que " + str(product.inventory)+" de "+str(product)
                #     raise serializers.ValidationError(msg)
                store=item.product.product.store_id
                # print("******************************")
                # print(store)
                prod_qty_updated=product.inventory - item.quantity
                Aprod.objects.filter(id= product.id).update(inventory=prod_qty_updated)

                if prod_qty_updated==0:
                    print("this product is out of stock!!!!")
                    Aprod.objects.filter(id= product.id).update(is_active=False)
                    if not Aprod.objects.filter(is_active=True).filter(product_id=product.product.id).exists():
                        Product.objects.filter(id=product.product_id).update(is_active=False)
                        msg="Votre vitrine " + str(item.product.product.title) + " est en rupture de stock!!!"
                        # CartItem.objects.filter(id=item.id).update(msg=msg,store=store)
                        
                    msg="Votre produit " +str(item.product.slug) + " est en rupture de stock!!!"
                    # CartItem.objects.filter(id=item.id).update(msg=msg,store=store)
                    
                elif prod_qty_updated <3:
                    msg= "Attension!!! la quantité de votre produit " + str(item.product.slug) + " est inférieur à 3 pièces !!!"
                    # CartItem.objects.filter(id=item.id).update(msg=msg,store=store)
                # print("2222222222222222")
                # print(store)
                # print(item.store)
                # Store.objects.filter(user= store.user).update(order_count=order_count,membership=membership)
                item.store=store
                item.msg=msg

                

            order_items =[
                OrderItem(
                    order=order,
                    product = item.product,
                    unit_price=item.product.product.price_with_promotion,
                    quantity= item.quantity,
                    msg=item.msg,
                    store=item.store
                )for item in cart_items
            ]
            print(order_items)
            print(order_items[0].product.product)#anaghim 's store
            print(order_items[0].product.product.store)#anaghim 's store
            print(order_items[0].product.product.store.user)# anaghimbensouissi@gmail.com
            for item in order_items:
                store=item.product.product.store
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

class SimpleSubCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCollection
        fields=['id','title']
class ListCollectionSerializer(serializers.ModelSerializer):
    SubCollections =SimpleSubCollectionSerializer(many=True, read_only=True) 
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