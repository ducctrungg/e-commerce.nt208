function updateCookieItem(data) {
  let [productID, quantity, action] = [data['id'], data['quantity'], data['action']]
  if (action === 'add') {
    if (cart[productID] == undefined) {
      cart[productID] = { 'quantity': 1 }
    }
    else {
      cart[productID]['quantity'] += 1
    }
  }
  if (action === 'change') {
    cart[productID]['quantity'] = quantity
    if (cart[productID]['quantity'] <= 0) {
      delete cart[productID]
    }
  }
  if (action === 'remove') {
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
    return result;
  } catch (error) {
    console.error("Error:", error);
  }
}
