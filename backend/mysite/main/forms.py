from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','description','image','type']

class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exculde = ['user']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']