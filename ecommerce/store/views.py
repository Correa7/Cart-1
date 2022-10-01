from django.shortcuts import render
from .models import *

# from django.contrib.auth.decorators import login_required


# Create your views here.


def store(request):
     products = Products.objects.all()
     context = {"products": products}
     return render(request, 'store/store.html', context)



# @login_required
def cart(request):
     
     if request.user.is_authenticated:        ## una manera de verificar si esta logueado otra seria con el decorador @login_required##
          customer = request.user.customer

          order, created = Order.objects.get_or_create( customer=customer, complete=False)   # .get_or_create() estmos consultando si el cliente tiene un pedido y/o lo creamos#
                                   # pasamos al cliente com parametro, y complete=False por que el pedido esta abierto aun##
                         
          items = order.orderitem.all() #de lo anterior recuperamos el pedido y aqui sus items, order.orderitem.all() orderitem es el related_name que le pusimos##

     else:
          items = []
          order = {'get_cart_total':0 , 'get_cart_item':0} #se crea un carro vacio por si no esta logueado el usuario#

     context = {'items': items,'order': order }
     return render(request, 'store/cart.html', context)
     

def checkout(request):

     if request.user.is_authenticated:        #mismo que en def cart #####

          customer = request.user.customer
          order, created = Order.objects.get_or_create( customer=customer, complete=False)             
          items = order.orderitem.all() 

     else:
          items = []
          order = {'get_cart_total':0 , 'get_cart_item':0}

     context = {'items': items,'order': order }
     return render(request, 'store/checkout.html', context)