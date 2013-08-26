# djpg

`djpg` is a Django module that integrates with the online payment service [PagSeguro](https://pagseguro.uol.com.br/).


## Installation

Simply:

```bash
$ pip install djpg
```
Or:

```bash
$ pip install -e git+https://github.com/mstrcnvs/djpg.git@master#egg=djpg
```


## Examples

### Creating a cart and redirecting the user

```python
import djpg

def my_view(request):
	cart = djpg.Cart(reference='1234', redirect_url='https://mysite.com/')
	item = djpg.Item(id='1', description='Cool T-shirts!', amount=25.00, quantity=2)
	cart.add_item(item)

	code = cart.checkout()
	if code:
		# This will redirect the user to PagSeguro's checkout page
		# so the cart can be paid, or canceled.
		return cart.proceed(code)
```

### Receiving notifications

This snippet will ensure `djpg` receives notifications from PagSeguro and dispatch them to the respective signals. This endpoint needs to be configured in your PagSeguro's account also, under "Notificações de Transações" (e.g.: https://mysite.com/pagseguro/notifications/).

```python
urlpatterns += patterns('',
	url(r'^pagseguro/', include('djpg.urls'))
)
```

Then you can connect listeners to the signals that are relevant to you.

```python
from djpg.signals import transaction_paid

def on_paid(sender, **kwargs):
	transaction = kwargs.pop('transaction')
	ref = transaction['reference']
	info = transaction['anotherinfo']
	do_something()

transaction_paid.connect(on_paid)
```

The available signals are:
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
