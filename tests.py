#!/usr/bin/env python
# coding: utf-8

import os
import unittest

# Allow tests to run without a settings.py file
from django.conf import settings
if not settings.configured:
    settings.configure(
        PAGSEGURO_EMAIL=os.environ['PAGSEGURO_EMAIL'],
        PAGSEGURO_TOKEN=os.environ['PAGSEGURO_TOKEN'],
        PAGSEGURO_SANDBOX='PAGSEGURO_SANDBOX' in os.environ
    )

import djpg


class DjpgTestCase(unittest.TestCase):
    def test_entry_points(self):
        djpg.Item
        djpg.Cart
        djpg.Transaction
        djpg.Notification
        djpg.codes
        djpg.signals

    def test_item(self):
        djpg.Item(id=3, amount=19.50, description='Cool T-shirt!', weight=1000,
                  shipping_cost=9.90)

    def test_cart(self):
        djpg.Cart(reference='...', currency='BRL',
                  redirect_url='http://foo.com', max_age=1200, max_uses=10)

    def test_cart_add_item(self):
        cart = djpg.Cart(reference='...')
        item = djpg.Item(id=3, amount=19.50)
        cart.add_item(item)

        self.assertEqual(len(cart.get_items()), 1)

    def test_cart_add_items(self):
        cart = djpg.Cart(reference='...')
        st_item = djpg.Item(id=1, amount=19.50)
        nd_item = djpg.Item(id=2, amount=19.50)
        cart.add_items(st_item, nd_item)

        self.assertEqual(len(cart.get_items()), 2)

    def test_cart_add_something_else(self):
        cart = djpg.Cart(reference='...')

        with self.assertRaises(TypeError):
            cart.add_item(123)
            cart.add_item('...')
            cart.add_item({1: 2})
            cart.add_item([1, 2, 3])

    def test_cart_checkout_without_items(self):
        cart = djpg.Cart(reference='...')

        with self.assertRaises(djpg.exceptions.PagSeguroInvalidRequestException):
            cart.get_checkout_code()

    def test_cart_checkout(self):
        cart = djpg.Cart(reference='...')
        item = djpg.Item(id=1, amount=19.50)
        cart.add_item(item)

        checkout_code = cart.get_checkout_code()

        self.assertIsNotNone(checkout_code)

    def test_cart_checkout_invalid_data(self):
        cart = djpg.Cart(reference='...', sender_phone='abcd')
        item = djpg.Item(id=1, amount=19.50)
        cart.add_item(item)

        with self.assertRaises(djpg.exceptions.PagSeguroInvalidRequestException):
            cart.get_checkout_code()

    def test_cart_checkout_url(self):
        cart = djpg.Cart(reference='...')
        item = djpg.Item(id=1, amount=19.50)
        cart.add_item(item)

        checkout_code = cart.get_checkout_code()
        checkout_url = cart.get_checkout_url(checkout_code)

        self.assertIsNotNone(checkout_url)
        self.assertIn('http', checkout_url)

    def test_notification(self):
        djpg.Notification('123456')
        djpg.Notification('123456', type='transaction')
        djpg.Notification(code='123456')
        n = djpg.Notification(code='123456', type='transaction')

        self.assertIsNotNone(str(n))

    def test_invalid_notification(self):
        n = djpg.Notification('123456')

        with self.assertRaises(djpg.exceptions.PagSeguroInvalidRequestException):
            n.get_data()

    def test_transaction(self):
        djpg.Transaction('123456')
        djpg.Transaction(code='123456')

        t = djpg.Transaction('123456')

        self.assertIsNotNone(str(t))

    def test_invalid_transaction(self):
        t = djpg.Transaction('123456')

        with self.assertRaises(djpg.exceptions.PagSeguroInvalidRequestException):
            t.get_data()


if __name__ == '__main__':
    unittest.main()
