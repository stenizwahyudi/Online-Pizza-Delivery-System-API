# coding: utf-8

from __future__ import absolute_import

import requests
import datetime

from flask import json
from six import BytesIO

from swagger_server.models.transactions import Transactions  # noqa: E501
from swagger_server.test import BaseTestCase


class TestTransactionsController(BaseTestCase):
    """TransactionsController integration test stubs"""

    order_id = 0
    store_id = 0

    def test_create_receipt(self):
        """Test case for create_receipt

        Purchase an order.
        """
        global store_id, order_id
        url = 'https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/stores'
        data = {
            "pizza_stores_id": 37,
            "specials": [
                1,
                2,
                3
                ],
            "store_location": "225 Terry Ave, Seattle, WA 98109",
            "store_name": "Turing Pizza NEU Seattle"
            }
        response = requests.post(url, json=data)
        result = response.json()
        store_id = result['pizza_stores_id']
        assert response.status_code == 200
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/orders"
        data = {
            "orders_id": 1,
            "pizza_store_id": store_id,
            "pizzas_id": [
                1,
                2,
                3
                ],
            "total_price": 29.99
            }
        response = requests.post(url, json=data)
        result = response.json()
        order_id = result['orders_id']
        assert response.status_code == 200
        today = datetime.datetime.now()
        url = 'https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/receipts?pizzaOrderId='
        data = {
            "card_billing_address": "101 Dexter Ave",
            "card_cvc": "1234",
            "card_expiration_month": "1",
            "card_expiration_year": str(today.year + 1),
            "card_number": "1234567890000000",
            "city": "Seattle",
            "name": "Henry",
            "order_time": "1995-09-07T10:40:52Z",
            "phone_number": "7777777777",
            "pizza_order_id": 1,
            "pizza_receipt_id": 12345634,
            "state": "WA",
            "zip_code": "98109"
            }
        response = requests.post(url + str(order_id), json=data)
        assert response.status_code == 404
        data = {
            "card_billing_address": "101 Dexter Ave",
            "card_cvc": "12a",
            "card_expiration_month": "1",
            "card_expiration_year": str(today.year + 1),
            "card_number": "1234567890000000",
            "city": "Seattle",
            "name": "Henry",
            "order_time": "1995-09-07T10:40:52Z",
            "phone_number": "7777777777",
            "pizza_order_id": 1,
            "pizza_receipt_id": 12345634,
            "state": "WA",
            "zip_code": "98109"
            }
        response = requests.post(url + str(order_id), json=data)
        assert response.status_code == 404
        data = {
            "card_billing_address": "101 Dexter Ave",
            "card_cvc": "123",
            "card_expiration_month": "0",
            "card_expiration_year": "2022",
            "card_number": "1234567890000000",
            "city": "Seattle",
            "name": "Henry",
            "order_time": "1995-09-07T10:40:52Z",
            "phone_number": "7777777777",
            "pizza_order_id": 1,
            "pizza_receipt_id": 12345634,
            "state": "WA",
            "zip_code": "98109"
            }
        response = requests.post(url + str(order_id), json=data)
        assert response.status_code == 404
        data = {
            "card_billing_address": "101 Dexter Ave",
            "card_cvc": "123",
            "card_expiration_month": "15",
            "card_expiration_year": "2022",
            "card_number": "1234567890000000",
            "city": "Seattle",
            "name": "Henry",
            "order_time": "1995-09-07T10:40:52Z",
            "phone_number": "7777777777",
            "pizza_order_id": 1,
            "pizza_receipt_id": 12345634,
            "state": "WA",
            "zip_code": "98109"
            }
        response = requests.post(url + str(order_id), json=data)
        assert response.status_code == 404
        data = {
            "card_billing_address": "101 Dexter Ave",
            "card_cvc": "123",
            "card_expiration_month": str(today.month - 1),
            "card_expiration_year": str(today.year),
            "card_number": "1234567890000000",
            "city": "Seattle",
            "name": "Henry",
            "order_time": "1995-09-07T10:40:52Z",
            "phone_number": "7777777777",
            "pizza_order_id": 1,
            "pizza_receipt_id": 12345634,
            "state": "WA",
            "zip_code": "98109"
            }
        response = requests.post(url + str(order_id), json=data)
        assert response.status_code == 404
        data = {
            "card_billing_address": "101 Dexter Ave",
            "card_cvc": "123",
            "card_expiration_month": "10",
            "card_expiration_year": str(today.year + 1),
            "card_number": "123456789000000",
            "city": "Seattle",
            "name": "Henry",
            "order_time": "1995-09-07T10:40:52Z",
            "phone_number": "7777777777",
            "pizza_order_id": 1,
            "pizza_receipt_id": 12345634,
            "state": "WA",
            "zip_code": "98109"
            }
        response = requests.post(url + str(order_id), json=data)
        assert response.status_code == 404
        data = {
            "card_billing_address": "101 Dexter Ave",
            "card_cvc": "123",
            "card_expiration_month": "10",
            "card_expiration_year": str(today.year + 1),
            "card_number": "a234567890000000",
            "city": "Seattle",
            "name": "Henry",
            "order_time": "1995-09-07T10:40:52Z",
            "phone_number": "7777777777",
            "pizza_order_id": 1,
            "pizza_receipt_id": 12345634,
            "state": "WA",
            "zip_code": "98109"
            }
        response = requests.post(url + str(order_id), json=data)
        assert response.status_code == 404
        data = {
            "card_billing_address": "101 Dexter Ave",
            "card_cvc": "123",
            "card_expiration_month": "10",
            "card_expiration_year": str(today.year + 1),
            "card_number": "1234567890000000",
            "city": "Seattle",
            "name": "Henry",
            "order_time": "1995-09-07T10:40:52Z",
            "phone_number": "777777777",
            "pizza_order_id": 1,
            "pizza_receipt_id": 12345634,
            "state": "WA",
            "zip_code": "98109"
            }
        response = requests.post(url + str(order_id), json=data)
        assert response.status_code == 404
        data = {
            "card_billing_address": "101 Dexter Ave",
            "card_cvc": "123",
            "card_expiration_month": "10",
            "card_expiration_year": str(today.year + 1),
            "card_number": "1234567890000000",
            "city": "Seattle",
            "name": "Henry",
            "order_time": "1995-09-07T10:40:52Z",
            "phone_number": "777777777a",
            "pizza_order_id": 1,
            "pizza_receipt_id": 12345634,
            "state": "WA",
            "zip_code": "98109"
            }
        response = requests.post(url + str(order_id), json=data)
        assert response.status_code == 404
        data = {
            "card_billing_address": "101 Dexter Ave",
            "card_cvc": "123",
            "card_expiration_month": "10",
            "card_expiration_year": str(today.year + 1),
            "card_number": "1234567890000000",
            "city": "Seattle",
            "name": "Henry",
            "order_time": "1995-09-07T10:40:52Z",
            "phone_number": "7777777777",
            "pizza_order_id": order_id,
            "pizza_receipt_id": 12345634,
            "state": "WA",
            "zip_code": "98109"
            }
        response = requests.post(url + str(order_id), json=data)
        assert response.status_code == 200
        data = {
            "card_billing_address": "101 Dexter Ave",
            "card_cvc": "123",
            "card_expiration_month": "10",
            "card_expiration_year": str(today.year + 1),
            "card_number": "1234567890000000",
            "city": "Seattle",
            "name": "Henry",
            "order_time": "1995-09-07T10:40:52Z",
            "phone_number": "7777777777",
            "pizza_order_id": order_id,
            "pizza_receipt_id": 12345634,
            "state": "WA",
            "zip_code": "98109"
            }
        response = requests.post(url + str(order_id), json=data)
        assert response.status_code == 400

    def test_get_receipts(self):
        """Test case for get_receipts

        Get all available receipts.
        """
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/receipts"
        response = requests.get(url)
        assert response.status_code == 200

    def test_get_receipt_by_order_id(self):
        """Test case for get_receipt_by_order_id

        Get receipt by Order ID.
        """
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/receipts/"
        response = requests.get(url + str(order_id))
        assert response.status_code == 200
        response = requests.get(url + str(order_id + 1))
        assert response.status_code == 404
