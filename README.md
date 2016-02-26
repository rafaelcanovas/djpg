# djpg

`djpg` is a Django module that integrates with the online payment service [PagSeguro](https://pagseguro.uol.com.br/).

It will not touch your database neither alter your Django installation, `djpg` simply provides the machinery for you to send and receive requests from PagSeguro in a clean and pythonic way.


## Installation

Simply run:

```bash
$ pip install djpg
```

After installing, the only configurations required are `PAGSEGURO_EMAIL` and `PAGSEGURO_TOKEN`. You should add them to your *settings.py* file. The first is your signup email from PagSeguro, the other is the token they'll give you when you have a *seller* account. For example:

```python
PAGSEGURO_EMAIL = 'john@example.com'
PAGSEGURO_TOKEN = '78W52AQQ9Q8Q7D45S98AS8715SAQLEB1'
```


## Usage

### Creating a cart and redirecting the user

```python
from djpg import Cart, Item

def my_checkout_view(request):
    cart = Cart(reference='myref123', redirect_url='https://mysite.com/')
    item = Item(id=1, amount=19.50, description='Cool T-shirts!', quantity=2)
    cart.add_item(item)

    code = cart.checkout()
    if code:
        # This will redirect the user to the checkout page,
        # where the cart can be paid.
        return cart.proceed(code)
```

### Receiving notifications

The following snippet will ensure `djpg` receives notifications from PagSeguro and dispatch them to the respective signals.

```python
urlpatterns += patterns('',
    url(r'^pagseguro/', include('djpg.urls'))
)
```

Keep in mind that this endpoint needs to be configured in your PagSeguro account also (e.g.: https://mysite.com/pagseguro/notifications/).
Then you can connect listeners to the signals that are relevant to you.

```python
from djpg.signals import transaction_paid

def on_paid(sender, **kwargs):
    transaction = kwargs.pop('transaction')
    ref = transaction['reference']
    status = transaction['status']
    # ...

transaction_paid.connect(on_paid)
```

The following signals are available:
- notification_received
- transaction_received
- transaction_waiting
- transaction_analysis
- transaction_paid
- transaction_available
- transaction_dispute
- transaction_returned
- transaction_canceled
- transaction_unknown
