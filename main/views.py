from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
import simplejson
import json
import datetime
from .models import *
from .utils import *
from .decorators import *
from .forms import *
# Create your views here.


def home(request):
    cartData = getCartData(request)

    products = Product.objects.all()  # SELECT ALL PRODUCTS FROM DATABASE
    context = {
        'products': products,
        'order': cartData['order'],
    }
    return render(request, 'main/home.html', context)


def productDetails(request, slug):
    # SELECT a product that has the same slug as the slug from URL
    product = Product.objects.get(slug=slug)
    context = {'product': product}
    return render(request, 'main/product.html', context)


@unauthenticated_user   # only allow unauthenticated user use login module
def loginPage(request):
    if request.method == 'POST':    # If receive data from user, authenticate user
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:    # If user is valid, login
                login(request, user)
                return redirect('home')
            else:                   # If show out error
                messages.info(request, 'Username or Password is incorrect')
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {"form": form})


@login_required(login_url='login')  # need to login for logout module
def logoutUser(request):
    logout(request)
    return redirect('home')


@unauthenticated_user  # only allow unauthenticated user use login module
def registerPage(request):
    if request.method == 'POST':    # If receive data from user
        form = RegisterForm(request.POST)
        if form.is_valid():  # validate username and password1, password2 | password2 is password confirm
            register = form.save(commit=False)
            usercreate = User.objects.create_user(username=form.cleaned_data["name"],
                                                  password=form.cleaned_data["password1"])
            usercreate.save()
            user = User.objects.get(username=form.cleaned_data["name"])
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            register.user = user
            register.save()
            messages.success(
                request, 'Account was created for ' + register.name)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html',  {"form": form})


@login_required(login_url='login')   # need to login for account module
def accountPage(request):
    customer = request.user.customer    # render the page base on user
    if request.method == 'POST':
        password = request.POST.get('password')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        if not validate_name(name):  # validate data
            messages.error(request, 'Invalid name')
            return redirect('account')
        if not validate_email(email):
            messages.error(request, 'Invalid email address')
            return redirect('account')
        if not validate_phone(phone):
            messages.error(request, 'Invalid phone number')
            return redirect('account')
        if password != "":  # check if the password changed | if changed set new password | if not skip set new password
            customer.user.set_password(password)
        customer.name = name
        customer.email = email
        customer.phone = phone
        customer.save()
        return redirect('account')
    context = {
        'customer': customer
    }
    return render(request, 'main/account.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])  # only allow admin
def adminPage(request):
    customers = Customer.objects.all()
    products = Product.objects.all()
    orderitems = OrderItem.objects.all()
    orders = Order.objects.all()
    total_orders = 0
    total_income = 0
    orders_pending = 0
    orders_completed = 0
    for order in orders:    # Sum all order data in database
        if order.complete == False:
            orders_pending += 1
        if order.complete == True:
            orders_completed += 1
            total_income += order.get_cart_total
        total_orders += 1
    if request.method == 'POST':
        if 'productType_submit' in request.POST:
            # get product type from user for searching
            product_type = request.POST.get('product_type')
            if product_type == "":
                messages.error(request, 'Empty product type')
            else:
                products = Product.objects.filter(type=product_type)
        if 'dateOrdered_submit' in request.POST:
            date_ordered = request.POST.get('date_ordered')
            if date_ordered != "":
                total_orders = 0
                total_income = 0
                orders_pending = 0
                orders_completed = 0
                temp = []
                for order in orders:
                    if date_ordered == order.date_ordered.strftime('%d/%m/%Y'):
                        if order.complete == False:
                            orders_pending += 1
                        if order.complete == True:
                            orders_completed += 1
                            total_income += order.get_cart_total
                        total_orders += 1
                        temp.append(order)
                orders = temp

    context = {
        'customers': customers,
        'products': products,
        'orderitems': orderitems,
        'orders': orders,
        'total_orders': total_orders,
        'total_income': total_income,
        'orders_completed': orders_completed,
        'orders_pending': orders_pending,
    }
    return render(request, 'main/admin.html', context)


def cart(request):
    cartData = getCartData(request)

    context = {
        'items': cartData['items'],
        'order': cartData['order'],
    }
    return render(request, 'main/cart.html', context)


# need login for checkout module | only authenticated user can checkout
@login_required(login_url='login')
def checkout(request):
    cartData = getCartData(request)

    context = {
        'items': cartData['items'],
        'order': cartData['order'],
    }
    return render(request, 'main/checkout.html', context)


@login_required(login_url='login')
# update cart for authenticated user | unauthenticated user use cookie cart
def updateItem(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        customer = request.user.customer
        product = Product.objects.get(id=data['id'])
        order, _ = Order.objects.get_or_create(
            customer=customer, complete=False)
        orderItem, _ = OrderItem.objects.get_or_create(
            order=order, product=product)
        if data['action'] == 'change':
            orderItem.quantity = data['quantity']
        elif data['action'] == 'add':
            orderItem.quantity += 1
        elif data['action'] == 'minus':
            orderItem.quantity -= 1
        orderItem.date_added = datetime.datetime.now()
        orderItem.save()
        if orderItem.quantity <= 0:
            orderItem.delete()  

        tmp = model_to_dict(order, exclude="date_ordered")
        tmp['get_cart_total'] = order.get_cart_total
        tmp['get_cart_items'] = order.get_cart_items
        context = {
            'status': "Success",
            'order': tmp,
            'item': model_to_dict(orderItem, exclude="date_added"),
        }
    return HttpResponse(simplejson.dumps(context), content_type="application/json")


@login_required(login_url='login')
def processOrder(request):  # save order for checkout
    if request.method == 'POST':
        customer = request.user.customer
        order, _ = Order.objects.get_or_create(
            customer=customer, complete=False)
        order.address = request.POST.get('address')
        order.complete = True
        transaction_id = datetime.datetime.now().timestamp()
        order.transaction_id = transaction_id
        order.date_ordered = datetime.datetime.now()
        order.save()
        return redirect(' ')
    return JsonResponse("Payment submitted", safe=False)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request):   # admin create
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin')

    context = {
        'form': form,
    }
    return render(request, 'main/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrderItem(request):   # admin create
    form = OrderItemForm()
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if quantity <= 0:
                messages.error(request, 'Invalid order item quantity')
                return redirect('create_orderitem')
            form.save()
            return redirect('admin')

    context = {
        'form': form,
    }
    return render(request, 'main/orderitem_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createProduct(request):  # admin create
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            if price < 0:   # validate data
                messages.error(request, 'Invalid product price')
                return redirect('create_product')
            form.save()
            product = Product.objects.get(name=name)
            product.slug = slugify(name)
            product.save()
            return redirect('admin')
    context = {
        'form': form,
    }
    return render(request, 'main/product_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createCustomer(request):    # admin create
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():  # validate data
            name = form.cleaned_data.get('username')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            if not validate_email(email):  # validate data
                messages.error(request, 'Invalid email address')
                return redirect('create_customer')
            if not validate_phone(phone):
                messages.error(request, 'Invalid phone number')
                return redirect('create_customer')
            form.save()
            user = User.objects.get(username=name)
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            customer = Customer.objects.create(
                user=user, email=email, phone=phone, name=name)
            customer.save()
            messages.success(request, 'Account was created for ' + name)
            return redirect('admin')

    context = {'form': form}
    return render(request, 'main/register.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):   # admin update
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    orderitems = order.orderitem_set.all()
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():  # validate data
            form.save()
            return redirect('admin')

    context = {
        'form': form,
        'orderitems': orderitems,
        'order': order

    }
    return render(request, 'main/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrderItem(request, pk):   # admin update
    orderItem = OrderItem.objects.get(id=pk)
    form = OrderItemForm(instance=orderItem)

    if request.method == 'POST':
        form = OrderItemForm(request.POST, instance=orderItem)
        if form.is_valid():  # validate data
            quantity = form.cleaned_data['quantity']
            if quantity <= 0:  # validate data
                messages.error(request, 'Invalid order item quantity')
                # redirect to domain/update_orderitem/pk
                return redirect('update_orderitem', pk)
            form.save()
            return redirect('admin')

    context = {
        'form': form,
    }
    return render(request, 'main/orderitem_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateProduct(request, pk):  # admin update
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():  # validate data
            price = form.cleaned_data['price']
            if price < 0:  # validate data
                messages.error(request, 'Invalid product price')
                # redirect to domain/update_product/pk
                return redirect('update_product', pk)
            product.slug = slugify(form.cleaned_data['name'])
            form.save()
            return redirect('admin')
    context = {
        'form': form,
        'slug': product.slug
    }
    return render(request, 'main/product_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateCustomer(request, pk):    # admin update
    user = User.objects.get(id=pk)
    customer = Customer.objects.get(user=user)
    if request.method == 'POST':
        password = request.POST.get('password')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        if not validate_name(name):  # validate data
            messages.error(request, 'Invalid name')
            # redirect to domain/update_customer/pk
            return redirect('update_customer', pk)
        if not validate_email(email):
            messages.error(request, 'Invalid email address')
            return redirect('update_customer', pk)
        if not validate_phone(phone):
            messages.error(request, 'Invalid phone number')
            return redirect('update_customer', pk)
        if password != "":  # check if the password changed| if changed set new password | if not skip set new password
            user.set_password(password)
        customer.name = name
        customer.email = email
        customer.phone = phone
        customer.save()
        user.save()
        return redirect('admin')
    context = {
        'user': user,
        'customer': customer
    }
    return render(request, 'main/customer_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):   # admin delete
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('admin')
    context = {
        'item': order
    }
    return render(request, 'main/delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteCustomer(request, pk):    # admin delete
    customer = User.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('admin')
    context = {
        'item': customer
    }
    return render(request, 'main/delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteProduct(request, pk):  # admin delete
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('admin')
    context = {
        'item': product
    }
    return render(request, 'main/delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrderItem(request, pk):   # admin delete
    orderItem = OrderItem.objects.get(id=pk)
    if request.method == 'POST':
        orderItem.delete()
        return redirect('admin')
    context = {
        'item': orderItem
    }
    return render(request, 'main/delete.html', context)


def dashboardPage(request):
    return render(request, 'main/dashboard.html')

def handling_404Page(request, exception):
    context = {}
    return render(request, 'main/404Page.html', context)
