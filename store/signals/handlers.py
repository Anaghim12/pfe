from email.message import EmailMessage
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
# from django.utils.html import strip_tags
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from store.models import Customer, Store
from store.signals import order_created
from store.models import OrderItem , Product, Collection , SubCollection
from django.utils.text import slugify
from test_project.utils import unique_slug_generator

# 
from django .template.loader import render_to_string


# we define a handler that create a store automatically when a user is created + he is a vendeur (.type ==4)(voir bd pour mieux comprendre : type_id =4 pour un type =2 qui on le suppose un vendeur)
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, **kwargs):
    if kwargs['created']:
        user=kwargs['instance']
        print(user.type) #2
        # print(user.type.role) #2
        # print(user.type_id)#4
        store_name=user.first_name +' ' + user.last_name +' store'
        if user.type_id ==4 :
            Store.objects.create(user=kwargs['instance'],store_name=store_name)
# on va automatiser la création d'un profil (mais en cas de passage d'un ordre par un client on doit protéger le route:orders/add  fil views.py pour obligé le client de terminer à remplir son profil avant de passé une commande  )
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, **kwargs):
    if kwargs['created']:
        user=kwargs['instance']
        Customer.objects.create(user=user)

#auto slug
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
    print('pre save')
    if instance.slug is None :
        instance.slug = unique_slug_generator(instance)



# we create a hander to handle a signal when "order_created " signal is created
@receiver(order_created)
def on_order_created(sender, **kwargs):
    order=kwargs['order']
    print(order)
    capture_email= order.customer.user.email
    name= order.customer.user.username
    title= 'Merci bien Mr/Mme ' + name
    order_items=OrderItem.objects.filter(order=order)
    # product=[]
    # for item in order_items:
    #     product.append(item.product.title)

    # print(product)
    # product=[]
    # for item in order_items:
    #     Product.objects.filter(id=item.product)    

    # qty management
    for item in order_items:
        product=item.product
        prod_qty_updated=product.inventory - item.quantity
        Product.objects.filter(id= product.id).update(inventory=prod_qty_updated)

        if prod_qty_updated==0:
            print("this product is out of stock!!!!")
            Product.objects.filter(id= product.id).update(is_active=False)
        elif prod_qty_updated <3:
            msg= "Attension!!! la quantité de votre produit " + str(item.product) + "devient inférieur à 3 pièces !!!"

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