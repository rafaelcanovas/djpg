try:
    from urlparse import urljoin  # Python 2
except ImportError:
    from urllib.parse import urljoin  # Python 3

import requests
import xmltodict

from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured

from djpg.exceptions import PagSeguroUnauthorizedException, \
    PagSeguroInvalidRequestException

try:
    PAGSEGURO_EMAIL = settings.PAGSEGURO_EMAIL
    PAGSEGURO_TOKEN = settings.PAGSEGURO_TOKEN
except AttributeError:
    raise ImproperlyConfigured('PagSeguro email or token missing')

PAGSEGURO_SANDBOX = getattr(settings, 'PAGSEGURO_SANDBOX', True)
DEFAULT_CHARSET = getattr(settings, 'DEFAULT_CHARSET', 'UTF-8')

CHECKOUT_URL = (
    'https://ws.sandbox.pagseguro.uol.com.br/v2/checkout/'
    if PAGSEGURO_SANDBOX else
    'https://ws.pagseguro.uol.com.br/v2/checkout/'
)
PAYMENT_URL = (
    'https://sandbox.pagseguro.uol.com.br/v2/checkout/payment.html'
    if PAGSEGURO_SANDBOX else
    'https://pagseguro.uol.com.br/v2/checkout/payment.html'
)
TRANSACTIONS_URL = (
    'https://ws.sandbox.pagseguro.uol.com.br/v2/transactions/'
    if PAGSEGURO_SANDBOX else
    'https://ws.pagseguro.uol.com.br/v2/transactions/'
)
NOTIFICATIONS_URL = (
    'https://ws.sandbox.pagseguro.uol.com.br/v2/transactions/notifications/'
    if PAGSEGURO_SANDBOX else
    'https://ws.pagseguro.uol.com.br/v2/transactions/notifications/'
)


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
    def __init__(self, reference, currency='BRL', **kwargs):
        session = requests.Session()
        session.headers['content-type'] = \
            'application/x-www-form-urlencoded; charset=' + DEFAULT_CHARSET
        session.params['email'] = PAGSEGURO_EMAIL
        session.params['token'] = PAGSEGURO_TOKEN
        session.params['reference'] = reference
        session.params['currency'] = currency

        optional_params = {
            'redirectURL': 'redirect_url',
            'notificationURL': 'notification_url',
            'maxAge': 'max_age',
            'maxUses': 'max_uses',
            'senderName': 'sender_name',
            'senderEmail': 'sender_email',
            'senderPhone': 'sender_phone',
            'senderAreaCode': 'sender_area_code',
            'senderCPF': 'sender_cpf',
            'senderBornDate': 'sender_born_date',
            'shippingType': 'shipping_type',
            'shippingCost': 'shipping_cost',
            'shippingAddressCountry': 'shipping_address_country',
            'shippingAddressState': 'shipping_address_state',
            'shippingAddressCity': 'shipping_address_city',
            'shippingAddressPostalCode': 'shipping_address_postal_code',
            'shippingAddressDistrict': 'shipping_address_district',
            'shippingAddressStreet': 'shipping_address_street',
            'shippingAddressNumber': 'shipping_address_number',
            'shippingAddressComplement': 'shipping_address_complement',
            'extraAmount': 'extra_amount',
        }

        for k, v in optional_params.items():
            try:
                session.params[k] = kwargs[v]
            except KeyError:
                pass

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

        if response.status_code == 401:
            raise PagSeguroUnauthorizedException()

        content = xmltodict.parse(response.content)

        if response.status_code == 200:
            return content['checkout']['code']
        elif response.status_code == 400:
            raise PagSeguroInvalidRequestException(
                code=content['errors']['error']['code'],
                msg=content['errors']['error']['message']
            )

    def proceed(self, code):
        endpoint = PAYMENT_URL + '?code=' + code
        return HttpResponseRedirect(endpoint)


class Transaction(object):
    def __init__(self, code):
        self.code = code

    def fetch_content(self):
        endpoint = urljoin(TRANSACTIONS_URL, self.code)
        params = {
            'email': PAGSEGURO_EMAIL,
            'token': PAGSEGURO_TOKEN
        }

        r = requests.get(endpoint, params=params)

        if r.status_code == 200:
            return xmltodict.parse(r.content, encoding='ISO-8859-1')


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
