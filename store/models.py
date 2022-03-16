from distutils.command.upload import upload
from tkinter import CASCADE
from wsgiref.validate import validator
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.
from django.db import models
#authentifications: creating user Profiles
from django.conf import settings
#pour interferer admin panel
from django.contrib import admin
#this is for manage our cart
from uuid import uuid4

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

class Collection(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    is_active =models.BooleanField(default=True)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+',blank=True)
    # cette fonction __str__ ans le but de retourner title de Collection in the damin panel
    def __str__(self):
        return self.title
    # to sort the collection in the admin title by the title
    class Meta:
        ordering=['title']
    class Meta:
        ordering=['title']
class SubCollection(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    is_active =models.BooleanField()
    collection =models.ForeignKey(Collection, on_delete = models.CASCADE,related_name='SubCollections')
    def __str__(self):
        return self.title
    
    class Meta:
        ordering=['title']

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
    store_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField(null=True) #qty
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT,related_name='products')
    promotions = models.ManyToManyField(Promotion,blank=True)
    characteristic = models.TextField() # les caractérique du produit comming from front "assurer le dynamisme"
    store = models.ForeignKey('Store',on_delete=models.CASCADE,related_name='products',default=4)
    sub_collection = models.ForeignKey('SubCollection',on_delete=models.CASCADE,related_name='products',default=1)
    def __str__(self):
        return self.title
    
    class Meta:
        ordering=['title']
class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='store/prod')

class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    photo =  models.ImageField(upload_to='store/customer/photo',blank=True)
    phone1 = models.CharField(max_length=255,blank=False)
    phone2 = models.CharField(max_length=255,blank=True)
    birth_date = models.DateField(null=True,blank=True)
    zipcode = models.CharField(max_length=100,blank=False,default='no post_code')
    street = models.CharField(max_length=255,blank=False,default='no street')
    city = models.CharField(max_length=255,blank=False,default='no city')
    #auth: create user profile
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # à gérer back selon des conditions
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    order_count =models.BigIntegerField()
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
    order_count =models.BigIntegerField(blank=True)
    description= models.TextField()
    brand = models.TextField(blank=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    #auth: create user profile
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.store_name
    
    class Meta:
        ordering=['store_name']
class StoreImage(models.Model):
    brand_image = models.ImageField(upload_to='store/brand')
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
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    # create custom permission in the admin panel
    class Meta:
        permissions =[
            ('cancel_order','can cancel order')
        ]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems') #par défaut on a orderitem_set
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        ordering=['order']

class Cart(models.Model):
    # this is to generate a uuid4 for id (for security resons )
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    # to make sure that there is no duplicate records for the same product in the same cart
    class Meta:
        unique_together =[['cart','product']]

class Slide(models.Model):
    slide_image = models.ImageField(upload_to='store/slide')

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

class StoreReview(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)