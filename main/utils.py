import json
from .models import *
import re
# this file contain ultils func for views.py file

def getCookieCartData(request):
    try:
        # take the data in the cookie field that has name is cart
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}

    for i in cart:
        try:
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'imageURL': product.imageURL,
                    'price': product.price,
                    'slug': product.slug,
                    'type': product.type
                },
                'quantity': cart[i]["quantity"],
                'get_total': total
            }
            items.append(item)
        except:
            pass

    return {'items': items, 'order': order}


def getCartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, _ = Order.objects.get_or_create(
            customer=customer, complete=False)
        # query orderitems that belong to the same order | 1 order contains many orderitem
        items = order.orderitem_set.all()
    else:
        cookieCartData = getCookieCartData(request)
        order = cookieCartData['order']
        items = cookieCartData['items']
    return {'order': order, 'items': items }


def validate_name(name):
    if name == "":  # if str is empty return false
        return False
    # if the string only contain word and space
    if not all(c.isalpha() or c.isspace() for c in name):
        return False
    return True


def validate_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def validate_phone(phone, length=10):
    if len(phone) < length:
        return False
    if phone.isdigit() and " " not in phone:
        return True
    else:
        return False
