from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import *
# Create your views here.

def home(request):
    cartData = getCartData(request)

    products= Product.objects.all() # SELECT ALL PRODUCTS FROM DATABASE
    context={
        'products':products,
        'order': cartData['order'],
    }
    return render(request, 'main/home.html', context)

def cart(request):
    cartData = getCartData(request)

    context={
        'items':cartData['items'],
        'order':cartData['order'],
    }
    return render(request, 'main/cart.html', context)

def checkout(request):
    cartData = getCartData(request)

    context={
        'items':cartData['items'],
        'order':cartData['order'],
    }
    return render(request, 'main/checkout.html', context)


def updateItem(request):
	data = json.loads(request.body)
	productID = data['productID']
	action = data['action']

	customer = request.user.customer
	product = Product.objects.get(id=productID)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    else:
        print("User not log in")
    return JsonResponse("Payment submitted",safe=False)