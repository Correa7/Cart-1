from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json

# from django.contrib.auth.decorators import login_required


# Create your views here.


def store(request):


     if request.user.is_authenticated:        #mismo que en def cart #####

          customer = request.user.customer
          order, created = Order.objects.get_or_create( customer=customer, complete=False)             
          items = order.orderitem.all()
          cartItems= order.get_cart_items 

     else:
          items = []
          order = {'get_cart_total':0 , 'get_cart_item':0}
          cartItems= order['get_cart_items']


     context = {'items': items,'order': order }
     products = Products.objects.all()
     context = {"products": products, 'cartItems': cartItems}
     # context = {"products": products}
     return render(request, 'store/store.html', context)



# @login_required
def cart(request):
     
     if request.user.is_authenticated:        ## una manera de verificar si esta logueado otra seria con el decorador @login_required##
          customer = request.user.customer

          order, created = Order.objects.get_or_create( customer=customer, complete=False)   # .get_or_create() estmos consultando si el cliente tiene un pedido y/o lo creamos#
                                   # pasamos al cliente com parametro, y complete=False por que el pedido esta abierto aun##
                         
          items = order.orderitem.all() #de lo anterior recuperamos el pedido y aqui sus items, order.orderitem.all() orderitem es el related_name que le pusimos##
          cartItems= order.get_cart_items 
     else:
          items = []
          order = {'get_cart_total':0 , 'get_cart_item':0} #se crea un carro vacio por si no esta logueado el usuario#
          cartItems= order['get_cart_items']
     context = {'items': items,'order': order, 'cartItems': cartItems }
     return render(request, 'store/cart.html', context)
     

def checkout(request):

     if request.user.is_authenticated:        #mismo que en def cart #####

          customer = request.user.customer
          order, created = Order.objects.get_or_create( customer=customer, complete=False)             
          items = order.orderitem.all() 
          cartItems= order.get_cart_items
     else:
          items = []
          order = {'get_cart_total':0 , 'get_cart_item':0}
          cartItems= order['get_cart_items']
     context = {'items': items,'order': order, 'cartItems': cartItems}
     return render(request, 'store/checkout.html', context)



def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Products.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItems.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)
