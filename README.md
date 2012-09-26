# djpg

`djpg` is a Django module that integrates with the online payment service [PagSeguro](https://pagseguro.uol.com.br/).

Sample:

```python
import djpg

cart = djpg.Cart(reference='1234', redirect_url='https://github.com/')
item = djpg.Item(id='1', description='Cool T-shirts!', amount=25.00, quantity=2)
cart.add_item(item)

code = cart.checkout()
if code:
	return cart.proceed(code)
```
