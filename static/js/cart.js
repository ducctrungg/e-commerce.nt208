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

async function updateUserOrder(data) {
  let url = '/update_item/'
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify(data),
    })
    const result = await response.json();
    $(".item-price").each(function () {
      if ($(this).find(':input').data("product") == result["item"]["product"]){
        $(this).find(".get_total").html(`$${(result["item"]["quantity"] * 100).toFixed(2)}`)
      }
    })
  } catch (error) {
    console.error("Error:", error);
  }
}


$().ready(function () {
  let listUpdate = $(".item-price")
  listUpdate.on('click', ':input', function (event) {
    event.preventDefault();
    let productId = $(this).data('product')
    let item = parseInt($(this).val())
    if (user === "AnonymousUser") {
      //for GUEST
      addCookieItem(productID, action)
    }
    else {
      //for USER
      updateUserOrder({ id: productId, quantity: item })
    }
  })
})


