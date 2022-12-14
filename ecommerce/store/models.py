from email.policy import default
from django.db import models
from django.contrib.auth.models import User 
# Create your models here.



#### Customer (cliente) ######

class Customer (models.Model):

    user = models.OneToOneField(User, on_delete = models.CASCADE, null=True, blank= True)
    name = models.CharField(max_length = 200, null=True)
    email = models.CharField(max_length = 200, null =True)

    def __str__(self):
        return self.name


##### Products ######33

class Products (models.Model):

    name = models.CharField (max_length = 200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False) ##por si el producto que vendemos es o no digital###
    image = models.ImageField (null=True, blank=True)

    def __str__(self):
        return self.name

##### Order ########

class Order (models.Model):

    customer = models.ForeignKey(Customer, on_delete= models.SET_NULL, null=True, blank=True) ##SET_NULL para que si se borra el cliente no se borre el registro de pedido###
    date_ordered = models.DateTimeField (auto_now_add =True)
    complete = models.BooleanField(default=False, null=True, blank= False)       #### instancia de comprobacion de si la orden finalizo, o se puede seguir agregando productos####
    transaction_id = models.CharField (max_length = 200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem.all()
        total = sum ([item.get_total for item in orderitems ])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem.all()
        total = sum ([item.quantity for item in orderitems ])
        return total

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping =True
            return shipping


##### OrderItems ####

class OrderItems (models.Model):
    product = models.ForeignKey(Products, on_delete= models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete= models.SET_NULL, null=True, blank=True, related_name='orderitem')
    quantity = models.IntegerField(default=0, null=True, blank= True)
    date_added= models.DateTimeField (auto_now_add =True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total



##### ShippingAddress (envios)#####

class ShippingAddress (models.Model):

    customer = models.ForeignKey(Customer, on_delete= models.SET_NULL, null=True, blank =True)
    order = models.ForeignKey(Order, on_delete= models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length = 200, null=False)
    city = models.CharField(max_length = 200, null=False)    ## null=) False por que son datos de envio deben ir si o si###
    state = models.CharField(max_length = 200, null=False)
    zipcode = models.CharField(max_length = 200, null=False) ## codigo postal###
    date_added= models.DateTimeField (auto_now_add =True)

    def __str__(self):
        return self.address

