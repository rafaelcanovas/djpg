from urlparse import urljoin

import requests
import xmltodict

from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured

try:
	PAGSEGURO_EMAIL = settings.PAGSEGURO_EMAIL
	PAGSEGURO_TOKEN = settings.PAGSEGURO_TOKEN
except AttributeError:
	raise ImproperlyConfigured('PagSeguro email or token missing')

DEFAULT_CHARSET = getattr(settings, 'DEFAULT_CHARSET', 'UTF-8')
CHECKOUT_URL = getattr(settings, 'PAGSEGURO_CHECKOUT_URL',
			'https://ws.pagseguro.uol.com.br/v2/checkout/')
PAYMENT_URL = getattr(settings, 'PAGSEGURO_PAYMENT_URL',
			'https://pagseguro.uol.com.br/v2/checkout/payment.html')
NOTIFICATIONS_URL = getattr(settings, 'PAGSEGURO_NOTIFICATIONS_URL',
			'https://ws.pagseguro.uol.com.br/v2/transactions/notifications/')


class Item(object):
	def __init__(self, id, amount, description='...', quantity=1, weight=None,
				shipping_cost=None):
		self.id = id
		self.amount = '%0.2f' % amount
		self.description = description
		self.quantity = quantity
		self.weight = weight
		self.shipping_cost = shipping_cost and ('%0.2f' % shipping_cost)


class Cart(object):
	def __init__(self, reference, currency='BRL', redirect_url=None,
				max_age=None, max_uses=None):
		session = requests.Session()
		session.headers['content-type'] = \
			'application/x-www-form-urlencoded; charset=' + DEFAULT_CHARSET
		session.params['email'] = PAGSEGURO_EMAIL
		session.params['token'] = PAGSEGURO_TOKEN
		session.params['reference'] = reference
		session.params['currency'] = currency

		if redirect_url:
			session.params['redirectURL'] = redirect_url
		if max_age:
			session.params['maxAge'] = max_age
		if max_uses:
			session.params['maxUses'] = max_uses

		self._items = []
		self._session = session

	def get_items(self):
		return self._items

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

			if v.weight:
				ret['itemWeight' + o] = v.weight
			if v.shipping_cost:
				ret['itemShippingCost' + o] = v.shipping_cost

		return ret

	def checkout(self):
		params = self.get_items_data()
		response = self._session.post(CHECKOUT_URL, params=params)

		if response.status_code == 200:
			content = xmltodict.parse(response.content)

			try:
				return content['checkout']['code']
			except KeyError:
				pass

	def proceed(self, code):
		endpoint = PAYMENT_URL + '?code=' + code
		return HttpResponseRedirect(endpoint)


class Notification(object):
	def __init__(self, type, code):
		self.type = type
		self.code = code

	def fetch_content(self):
		endpoint = urljoin(NOTIFICATIONS_URL, self.code)
		params = {
			'email': PAGSEGURO_EMAIL,
			'token': PAGSEGURO_TOKEN
		}

		r = requests.get(endpoint, params=params)

		if r.status_code == 200:
			return xmltodict.parse(r.content, encoding='ISO-8859-1')
