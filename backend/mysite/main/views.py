from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
import json
import datetime
from .models import *
from .utils import *
from .decorators import *
from .forms import *
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

@unauthenticated_user
def loginPage(request):
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
        
@unauthenticated_user
def registerPage(request):
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
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            customer = Customer.objects.create(user=user,email=email,phone=phone,name=name)
            customer.save()
            return redirect('login')
    
    context = {'form':form}
    return render(request, 'main/register.html', context)

@login_required(login_url='login')
def accountPage(request):
    context = {}
    return render(request, 'main/account.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def adminPage(request):
    customers = Customer.objects.all()
    products = Product.objects.all()
    orderitems = OrderItem.objects.all()
    orders = Order.objects.all()
    total_orders = 0
    orders_pending = 0
    orders_completed = 0
    for order in orders:
        if order.complete == False:
            orders_pending += 1
        if order.complete == True:
            orders_completed += 1
        total_orders += 1

    context = {
        'customers':customers,
        'products':products,
        'orderitems':orderitems,
        'orders':orders,
        'total_orders':total_orders,
        'orders_completed':orders_completed,
        'orders_pending':orders_pending,
    }
    return render(request, 'main/admin.html', context)

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

    orderItem.date_added = datetime.datetime.now()
    orderItem.save()
        
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

@login_required(login_url='login')
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
        order.date_ordered = datetime.datetime.now()
        order.save()
    else:
        print("User not log in")
    return JsonResponse("Payment submitted",safe=False)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin')
    
    context = {
        'form':form,
    }
    return render(request, 'main/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrderItem(request):
    form = OrderItemForm()
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin')
    
    context = {
        'form':form,
    }
    return render(request, 'main/orderitem_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createProduct(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            form.save()
            product = Product.objects.get(name=name)
            product.slug = slugify(name)
            product.save()
            return redirect('admin')
    context = {
        'form':form,
    }
    return render(request, 'main/product_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createCustomer(request):
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
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            customer = Customer.objects.create(user=user,email=email,phone=phone,name=name)
            customer.save()
            return redirect('admin')
    
    context = {'form':form}
    return render(request, 'main/register.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('admin')
    
    context = {
        'form':form,
    }
    return render(request, 'main/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrderItem(request, pk):
    orderItem = OrderItem.objects.get(id=pk)
    form = OrderItemForm(instance=orderItem)

    if request.method == 'POST':
        form = OrderItemForm(request.POST, instance=orderItem)
        if form.is_valid():
            form.save()
            return redirect('admin')
    
    context = {
        'form':form,
    }
    return render(request, 'main/orderitem_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateProduct(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product.slug = slugify(form.cleaned_data['name'])
            form.save()
            return redirect('admin')
    context = {
        'form':form,
        'slug':product.slug
    }
    return render(request, 'main/product_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateCustomer(request, pk):
    user = User.objects.get(id=pk)
    customer = Customer.objects.get(user=user)
    if request.method == 'POST':
        password = request.POST.get('password')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        #validate data before saving
        if password != "":
            user.set_password(password)

        customer.name = name
        customer.email = email
        customer.phone = phone
        customer.save()
        user.save()
        return redirect('admin')
    context = {
        'user':user,
        'customer':customer
    }
    return render(request, 'main/customer_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('admin')
    context = {
        'item':order
    }
    return render(request, 'main/delete.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteCustomer(request, pk):
    customer = User.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('admin')
    context = {
        'item':customer
    }
    return render(request, 'main/delete.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('admin')
    context = {
        'item':product
    }
    return render(request, 'main/delete.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrderItem(request, pk):
    orderItem = OrderItem.objects.get(id=pk)
    if request.method == 'POST':
        orderItem.delete()
        return redirect('admin')
    context = {
        'item':orderItem
    }
    return render(request, 'main/delete.html', context)

def dashboardPage(request):
    return render(request, 'main/dashboard.html')