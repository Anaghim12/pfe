from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.
from django.db import models
#authentifications: creating user Profiles
from django.conf import settings
#pour interferer admin panel
from django.contrib import admin
#this is for manage our cart
from uuid import uuid4
#to auto slugify our slug fields
from django.urls import reverse
class Collection(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True,null=True)
    is_active =models.BooleanField(default=True)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+',blank=True)
    # cette fonction __str__ ans le but de retourner title de Collection in the damin panel
    def __str__(self):
        return str(self.id)+ " " +self.title
    # to sort the collection in the admin title by the title
    class Meta:
        ordering=['title']
    class Meta:
        ordering=['title']
class SubCollection(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True,null=True)
    is_active =models.BooleanField(default=True)
    collection =models.ForeignKey(Collection,related_name='SubCollections', on_delete = models.CASCADE)
    def __str__(self):
        return str(self.collection_id) +" "+self.title
    
    class Meta:
        ordering=['collection_id']
class Aprod(models.Model):
    slug = models.SlugField(blank=True,null=True)
    inventory = models.IntegerField(default=1,blank=False,null=False)
    color = models.CharField(max_length=25,blank=False,null=False)
    size = models.PositiveSmallIntegerField(default=1,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    product=models.ForeignKey('Product',on_delete=models.CASCADE,related_name='a_prod')
    def __str__(self):
        return self.slug
class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True,null=True)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
    store_price = models.DecimalField(max_digits=6, decimal_places=2)
    # inventory = models.IntegerField(default=1) #qty
    price_with_promotion=models.DecimalField(max_digits=6, decimal_places=2,blank=True,null=True)
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT,related_name='products')
    # promotions = models.ManyToManyField(Promotion,blank=True)
    promotion= models.PositiveSmallIntegerField(default=0)
    # characteristic = models.TextField() # les caractérique du produit comming from front "assurer le dynamisme"
    material = models.CharField(default='coton',max_length=25)
    store = models.ForeignKey('Store',on_delete=models.CASCADE,related_name='products',default=4)
    is_active =models.BooleanField(default=False)
    sub_collection = models.ForeignKey('SubCollection',on_delete=models.CASCADE,related_name='products',default=1)
    # product_wishlist = models.ForeignKey('ProdWishList',on_delete=models.PROTECT,related_name='products',default=1)
    def get_absolute_url(self):
        return reverse("product-detail",kwargs={"pk":self.id})
    def __str__(self):
        return self.slug
    
    class Meta:
        ordering=['title']
    
# def product_post_save(*args,**kwargs):
#     print('pre_save')
#     print(args,kwargs)

# post_save.connect(product_post_save,sender=Product)
# def slug_generator(sender, instance, *args,**kwargs):
#     if not instance.slug:
#         instance.slug = 'SLUG'

# pre_save.connect(slug_generator, sender=Product)

class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='store/prod')
    def __str__(self):
        return str(self.image)
        
class ProdWishList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,primary_key=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def username(self):
        return self.user.username
    def __str__(self):
        return str(self.user)
class ProdItemWishList(models.Model):
    user = models.ForeignKey(ProdWishList, on_delete=models.CASCADE,related_name='prod_item_wish')
    products=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='prod_item_wish')
    note = models.IntegerField(default=5,blank =True,validators=[MinValueValidator(1),MaxValueValidator(5)])
    def username(self):
        return self.user.user.username
    def __str__(self):
        return str(self.user)
#manage store wishlist

class StoreWishList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,primary_key=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def username(self):
        return self.user.username
    def __str__(self):
        return str(self.user)
class StoreItemWishList(models.Model):
    user = models.ForeignKey(StoreWishList, on_delete=models.CASCADE,related_name='store_item_wish')
    store=models.ForeignKey('Store',on_delete=models.CASCADE,related_name='store_item_wish')
    note = models.IntegerField(blank=True, default=5,validators=[MinValueValidator(1),MaxValueValidator(5)])
    def username(self):
        return self.user.user.username
    def __str__(self):
        return str(self.store)

# class StoreWishList(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     note = models.IntegerField(null=True,validators=[MinValueValidator(1),MaxValueValidator(5)])

class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    photo =  models.ImageField(upload_to='store/customer/photo',blank=True,null=True)
    phone1 = models.CharField(max_length=255,blank=False)
    phone2 = models.CharField(max_length=255,blank=True,null=True)
    birth_date = models.DateField(null=True,blank=True)
    zipcode = models.CharField(max_length=100,blank=False,default='no post_code')
    street = models.CharField(max_length=255,blank=False,default='no street')
    city = models.CharField(max_length=255,blank=False,default='no city')
    #auth: create user profile
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True,on_delete=models.CASCADE, related_name='customer')
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer')

    # à gérer back selon des conditions
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    order_count =models.BigIntegerField(default=0,null=True,blank=True)
    # to combine the last and the first name in the admin pannel
    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'
    #auth: pour l'utliser fil customerAdmin 
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    @admin.display(ordering='user__last_name')
    def last_name (self):
        return self.user.last_name
    # the defaut sortering
    class Meta:
        ordering=['user__first_name','user__last_name']
class Store(models.Model):
    
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    store_name= models.CharField(max_length=255,blank=False)
    order_count =models.BigIntegerField(default=0,blank=True,null=True)
    description= models.TextField(blank=True,null=True)
    brand = models.TextField(blank=True,null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE,null=True,blank=True)
    
    #auth: create user profile
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True,on_delete=models.CASCADE, related_name='store')
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='store')

    def __str__(self):
        return self.store_name
    class Meta:
        ordering=['store_name']
class StoreImage(models.Model):
    #brand_image = models.ImageField(upload_to='store/brand')
    store_image = models.ImageField(upload_to='store/storee')
    store = models.ForeignKey(Store, on_delete=models.CASCADE,related_name='StoreImage')
class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT,related_name='order')
    
    # create custom permission in the admin panel
    class Meta:
        permissions =[
            ('cancel_order','can cancel order')
        ]

class DemandeRetour(models.Model):
    user = models.CharField(max_length=80)
    num_order = models.BigIntegerField()
    date_order = models.DateField()
    slug_produit_retour = models.CharField(max_length=255)
    cause = models.TextField(blank=False,null=False)
    image_facture = models.ImageField(upload_to='store/prod_retour')
    image_produit = models.ImageField(upload_to='store/prod_retour',null=True,blank=True)
    accept= models.BooleanField(default=False)
    refuse=models.BooleanField(default=False)
    placed_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Aprod, on_delete=models.PROTECT, related_name='orderitems') #par défaut on a orderitem_set
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    msg=models.CharField(max_length=255,default=" ",blank=True,null=True)
    store=models.BigIntegerField(default=1)
    class Meta:
        ordering=['order']

class Cart(models.Model):
    # this is to generate a uuid4 for id (for security resons )
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['-created_at']

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Aprod, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    msg=models.CharField(max_length=255,default=" ",blank=True,null=True)
    store=models.BigIntegerField(default=1)
    # to make sure that there is no duplicate records for the same product in the same cart
    # class Meta:
    #     unique_together =[['cart','product']]

class Slide(models.Model):
    slide_image = models.ImageField(upload_to='store/slide')

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    note = models.SmallIntegerField(default=1, validators=[MinValueValidator(1)] )    
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

class StoreReview(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    note = models.SmallIntegerField(default=1, validators=[MinValueValidator(1)] )    
    description = models.TextField()
    date = models.DateField(auto_now_add=True)