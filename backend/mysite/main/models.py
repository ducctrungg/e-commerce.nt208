from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    type = models.CharField(max_length=200, null=True)
    slug = models.SlugField(default="", null=False)
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url =''
        return url

    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True,null=True)
    address = models.CharField(max_length=200, null=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    date_ordered = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        total=0
        orderitems = self.orderitem_set.all()
        for item in orderitems:
            total += item.get_total
        return total
    
    @property
    def get_cart_items(self):
        total=0
        orderitems = self.orderitem_set.all()
        for item in orderitems:
            total += item.quantity
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True,null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True,null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = 0
        total = self.product.price * self.quantity
        return total

