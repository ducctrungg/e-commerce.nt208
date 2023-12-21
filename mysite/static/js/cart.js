let listUpdateItem = document.getElementsByClassName('update-cart')
Array.from(listUpdateItem).forEach(function (item) {
  item.addEventListener('click', function () {
    var productID = this.dataset.product
    var action = this.dataset.action
    if (user == "AnonymousUser") {
      //for GUEST
      addCookieItem(productID, action)
    }
    else {
      //for USER
      updateUserOrder(productID, action)
    }
  })
})

function addCookieItem(productID, action) {
  if (action == 'add') {
    if (cart[productID] == undefined) {
      cart[productID] = { 'quantity': 1 }
    }
    else {
      cart[productID]['quantity'] += 1
    }
  }

  if (action == 'remove') {
    cart[productID]['quantity'] -= 1
    if (cart[productID]['quantity'] <= 0) {
      delete cart[productID]
    }
  }
  document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
  location.reload()
}

function updateUserOrder(productID, action) {
  console.log('User is authenticated, sending data...')
  var url = '/update_item/'
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({ 'productID': productID, 'action': action })
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      location.reload()
    })
}
