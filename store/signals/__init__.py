from django.dispatch import Signal

#to create custom signal ==>aim: when we create an order we have signal to send an e-mail to our client 

order_created = Signal()
