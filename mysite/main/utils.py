import json
from .models import *

def getCookieCartData(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0}

    for i in cart:
        try:
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]

            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'imageURL':product.imageURL,
                    'price':product.price,
                },
                'quantity':cart[i]["quantity"],
                'get_total':total
            }
            items.append(item)
        except:
            pass
            
    return {'items':items,'order':order}


def getCartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        cookieCartData = getCookieCartData(request)
        order = cookieCartData['order']
        items = cookieCartData['items']
    return {'order':order,'items':items,}
