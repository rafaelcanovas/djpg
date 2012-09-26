from django.conf import settings
from django.http import HttpResponseRedirect

from furl import furl
import requests
import xmltodict


class Item(object):
	def __init__(self, id, description='', amount=0, quantity=1, weight=None,
				shipping_cost=None):
		self.id = id
		self.description = description
		self.amount = '%0.2f' % (amount,)
		self.quantity = quantity
		self.weight = weight
		self.shipping_cost = shipping_cost and ('%0.2f' % (shipping_cost,))


class Cart(object):
	def __init__(self, reference, currency='BRL', redirect_url=None,
				max_age=None, max_uses=None, email=None, token=None):
		self._data = {}
		self._items = []

		self._data['email'] = email or settings.PAGSEGURO_EMAIL
		self._data['token'] = token or settings.PAGSEGURO_TOKEN
		self._data['reference'] = reference
		self._data['currency'] = currency

		if redirect_url is not None:
			self._data['redirectUrl'] = redirect_url
		if max_age is not None:
			self._data['maxAge'] = max_age
		if max_uses is not None:
			self._data['maxUses'] = max_uses

		self.charset = getattr(settings, 'DEFAULT_CHARSET', 'UTF-8')
		self.checkout_url = getattr(settings, 'PAGSEGURO_CHECKOUT_URL',
				'https://ws.pagseguro.uol.com.br/v2/checkout/')
		self.payment_url = getattr(settings, 'PAGSEGURO_PAYMENT_URL',
				'https://pagseguro.uol.com.br/v2/checkout/payment.html')

	def add_item(self, item):
		if isinstance(item, Item):
			self._items.append(item)
		else:
			raise TypeError('%s expected got %s' %
							(Item.__name__, item.__class__.__name__))

	def add_items(self, *args):
		for item in args:
			self.add_item(item)

	def get_items_data(self):
		ret = {}
		for i, v in enumerate(self._items):
			o = str(i + 1)
			ret['itemId' + o] = v.id
			ret['itemDescription' + o] = v.description
			ret['itemAmount' + o] = v.amount
			ret['itemQuantity' + o] = v.quantity

			if v.weight is not None:
				ret['itemWeight' + o] = v.weight
			if v.shipping_cost is not None:
				ret['itemShippingCost' + o] = v.shipping_cost

		return ret

	def get_http_data(self):
		d = self._data.copy()
		d.update(self.get_items_data())
		return d

	def get_http_headers(self):
		return {'Content-Type':
				'application/x-www-form-urlencoded; charset=' + self.charset}

	def checkout(self):
		data = self.get_http_data()
		headers = self.get_http_headers()

		r = requests.post(self.checkout_url, data=data, headers=headers)

		if r.status_code == requests.codes.ok:
			content = xmltodict.parse(r.content)

			if content['checkout']:
				return content['checkout']['code']

	def proceed(self, code):
		return HttpResponseRedirect(furl(self.payment_url)
									.add(query_params={'code': code}).url)


class Notification(object):
	def __init__(self, type, code):
		self.type = type
		self.code = code

		self.notifications_url = getattr(settings,
			'PAGSEGURO_NOTIFICATIONS_URL',
			'https://ws.pagseguro.uol.com.br/v2/transactions/notifications')

	def fetch_content(self):
		f = furl(self.notifications_url).add(path=self.code)
		params = {
				'email': settings.PAGSEGURO_EMAIL,
				'token': settings.PAGSEGURO_TOKEN
		}

		r = requests.get(f.url, params=params)

		if r.status_code == requests.codes.ok:
			return xmltodict.parse(r.content)
