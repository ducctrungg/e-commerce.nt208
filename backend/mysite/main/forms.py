from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
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

class RegisterForm(UserCreationForm):
  class Meta:
      model = User
      fields = ['username','email','password1','password2'] 