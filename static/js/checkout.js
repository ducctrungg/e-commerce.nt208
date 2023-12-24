var total = '{{order.get_cart_total|floatformat:2}}'

if (user != "AnonymousUser") {
  document.getElementById('user-info').innerHTML = ''
}

var form = document.getElementById('form')
csrf_token = form.getElementsByTagName("input")[0].value

form.addEventListener('submit', function (e) {
  e.preventDefault()
  document.getElementById('form-button').classList.add('hidden')
  document.getElementById('payment-info').classList.remove('hidden')
})

document.getElementById('make-payment').addEventListener('click', function (e) {
  submitFormData()
})

function submitFormData() {
  var userFormData = {
    'name': null,
    'email': null,
    'total': total,
  }

  var shippingInfo = {
    'address': form.address.value,
  }

  if (user == "AnonymousUser") {
    userFormData.name = form.name.value
    userFormData.email = form.email.value
  }

  var url = "/process_order/"
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({ 'form': userFormData, 'shipping': shippingInfo }),

  })
    .then((response) => response.json())
    .then((data) => {
      console.log('Success:', data);
      alert('Transaction completed');
      cart = {}
      document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
      window.location.href = "{% url 'home' %}"
    })

}