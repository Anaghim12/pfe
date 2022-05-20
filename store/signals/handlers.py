from email.message import EmailMessage
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
# from django.utils.html import strip_tags
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from store.models import Customer, DemandeRetour, Store
from store.signals import order_created 
from store.models import OrderItem , Product, Collection , SubCollection,ProdWishList,StoreWishList, Cart, Aprod
from rest_framework import serializers
from test_project.utils import *
from uuid import uuid4
from rest_framework import generics
from store.serializers import OrderMsgSerializer
from store.models import Order
# 
from django .template.loader import render_to_string


# we define a handler that create a store automatically when a user is created + he is a vendeur (.type ==4)(voir bd pour mieux comprendre : type_id =4 pour un type =2 qui on le suppose un vendeur)
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, **kwargs):
    if kwargs['created']:
        user=kwargs['instance']
        print(user.type) #2
        # print(user.type.role) #2
        print(user.type_id)#4
        # print(user.store.store_name)
        
        store_name=user.first_name +' ' + user.last_name +' Boutique'
        if user.type_id ==4 :
            Store.objects.create(user=kwargs['instance'],store_name=store_name)
            print(user.store)
            print(user.store.store_name)
            Customer.objects.create(user=user)

# on va automatiser la création d'un profil (mais en cas de passage d'un ordre par un client on doit protéger le route:orders/add  fil views.py pour oblier le client de terminer à remplir son profil avant de faire passer une commande  )
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, **kwargs):
    if kwargs['created']:
        user=kwargs['instance']
        print(user.type_id)
        print(user.type)
        if user.type_id == 3:
            ProdWishList.objects.create(user=user)
            StoreWishList.objects.create(user=user)
            id = uuid4()
            Cart.objects.create(id=id)
            Customer.objects.create(user=user)
#affichage the right product
@receiver(post_save,sender=Aprod)
def create_slug_field(instance,sender,*args, **kwargs):
    prod_activation=instance.product.is_active
    if prod_activation == False :
        Product.objects.filter(id= instance.product_id).update(is_active=True)

#auto slug
#auto slug
@receiver(pre_save,sender=Aprod)
def create_slug_field(instance,sender,*args, **kwargs):
    if instance.slug is None :
        instance.slug = aprod_unique_slug_generator(instance)
@receiver(pre_save,sender=SubCollection)
def create_slug_field(instance,sender,*args, **kwargs):
    if instance.slug is None :
        instance.slug = unique_slug_generator(instance)
@receiver(pre_save,sender=Product)
def create_slug_field(instance,sender,*args, **kwargs):
    
    if instance.slug is None :
        instance.slug = unique_slug_generator(instance)
    print('there is a slug')
@receiver(pre_save,sender=Collection)
def create_slug_field(instance,sender, **kwargs):
    if instance.slug is None :
        instance.slug = unique_slug_generator(instance)
#demande de retourd produit est créer
@receiver(post_save,sender=DemandeRetour)
def create_demande_retour_prod(sender,instance, **kwargs):
    print('AVANT CONDITION')
    print(kwargs)
    mail=instance.user
    if kwargs['created']==False:
        print(instance.accept)
        print(instance.refuse)
        if instance.accept==True:
            print('**********accept demand')
            template= render_to_string('accepter.html')
            titre="Votre Demande a été accepté"   
        elif instance.refuse==True:
            print('**********refuse demand')
            template= render_to_string('refuser.html')
            titre= "Votre Demande a été refusé"
    else:
        print('**********demand envoyé')
        template= render_to_string('retourProd.html')
        titre="Demande de Retour de Produit est envoyée avec succèe"
    # text_content = strip_tags(template)

    email =EmailMessage(
    titre,
    template,
    settings.EMAIL_HOST_USER,
    [mail],
        
        )    
    email.fail_silently=False,
    email.send()



# we create a hander to handle a signal when "order_created " signal is created
@receiver(order_created)
def on_order_created(sender, **kwargs):
    order=kwargs['order']
    # if order.msg != "":
    #     class OrderMsg(generics.RetrieveAPIView):
    #         serializer_class = OrderMsgSerializer
    #         def get_queryset(self):
    #             return Order.objects.filter(order=order)
    print(order)
    capture_email= order.customer.user.email
    name= order.customer.user.username
    title= 'Merci bien Mr/Mme ' + name
    order_items=OrderItem.objects.filter(order=order)
    # product=[]
        # order_count = order_count+1


    #    product.append(item.product.title)

    # print(product)
    # product=[]
    # for item in order_items:
    #     Product.objects.filter(id=item.product)    

    # # qty management
    # for item in order_items:
    #     product=item.product
    #     if product.inventory < item.quantity:
    #         raise serializers.ValidationError('Désolé, vous pouvez acheter que ' + product.inventory+'!!!')
    #     prod_qty_updated=product.inventory - item.quantity
    #     Aprod.objects.filter(id= product.id).update(inventory=prod_qty_updated)

    #     if prod_qty_updated==0:
    #         print("this product is out of stock!!!!")
    #         Aprod.objects.filter(id= product.id).update(is_active=False)
    #         if not Aprod.objects.filter(is_active=True).filter(product_id=product.product.id).exists():
    #             Product.objects.filter(id=product.product_id).update(is_active=False)
    #             msg="Votre vitrine " + str(item.product.product.title) + "est en rupture de stock!!!"
    #             return msg
    #         msg="Votre produit " +str(item.product.slug) + "est en rupture de stock!!!"
    #         return msg
    #     elif prod_qty_updated <3:
    #         msg= "Attension!!! la quantité de votre produit " + str(item.product.slug) + "devient inférieur à 3 pièces !!!"

    template= render_to_string('index.html',{'order_items':order_items,'name':name})
    # text_content = strip_tags(template)

    email =EmailMessage(
        title,
        template,
        settings.EMAIL_HOST_USER,
        [capture_email],
        
    )    
    email.fail_silently=False,
    email.send()