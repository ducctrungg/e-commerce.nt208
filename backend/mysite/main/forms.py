from django.forms import ModelForm
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