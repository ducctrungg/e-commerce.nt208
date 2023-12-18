from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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

def productDetails(request, slug):
    product = Product.objects.get(slug=slug)

    context = {'product':product}
    return render(request, 'main/product.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR Password is in correct')

        context = {}
        return render(request, 'main/login.html', context)


def logoutUser(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')
        

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = UserCreationForm()
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                name = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + name)
                email = request.POST.get('email')
                phone = request.POST.get('phone')
                user = User.objects.get(username=name)
                customer = Customer.objects.create(user=user,email=email,phone=phone,name=name)
                customer.save()
                return redirect('login')
        
        context = {'form':form}
        return render(request, 'main/register.html', context)

def cart(request):
    cartData = getCartData(request)

    context={
        'items':cartData['items'],
        'order':cartData['order'],
    }
    return render(request, 'main/cart.html', context)

@login_required(login_url='login')
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
        order.address = data['shipping']['address']

        if total == order.get_cart_total:
            order.complete = True
        order.save()
    else:
        print("User not log in")
    return JsonResponse("Payment submitted",safe=False)