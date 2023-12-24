from django.forms import ModelForm
from django import forms
from .models import *
import re


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image', 'type']


class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'


class LoginForm (forms.Form):
    username = forms.CharField(label="username", max_length=200)
    password = forms.CharField(label="password", widget=forms.PasswordInput())


class RegisterForm (ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
                'required': True
            })
    password1 = forms.CharField(
        label="password1", widget=forms.PasswordInput())
    password2 = forms.CharField(
        label="password2", widget=forms.PasswordInput())

    class Meta:
        model = Customer
        fields = '__all__'

    def clean_email(self):
        email = self.cleaned_data["email"]
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, email):
            self.add_error("email", "Invalid email")
        return email

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if len(phone) != 10:
            self.add_error("phone", "Phonenumber must have 10 digits")
            return
        if not phone.isdigit():
            self.add_error("phone", "Phonenumber must only have number")
        return True

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            self.add_error("password1", "Password does not match")
            self.add_error("password2", "Password does not match")
