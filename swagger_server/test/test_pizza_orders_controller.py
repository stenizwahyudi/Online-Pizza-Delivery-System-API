# coding: utf-8

from __future__ import absolute_import

import requests
import pytest

from flask import json
from six import BytesIO

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.order import Order  # noqa: E501
from swagger_server.models.pizza import Pizza  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPizzaOrdersController(BaseTestCase):
    """PizzaOrdersController integration test stubs"""

    order_id = 0
    store_id = 0
    pizza_id = 0
    special_id = 0
    size_id = 0
    topping_id = 0

    @pytest.mark.run(order=1)
    def test_add_pizza_order(self):
        """Test case for add_pizza_order

        Create a new pizza order.
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
    
    @pytest.mark.run(order=2)
    def test_get_pizza_orders(self):
        """Test case for get_pizza_orders

        Get all pizza orders stored on the database.
        """
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/orders"
        response = requests.get(url)
        assert response.status_code == 200
    
    @pytest.mark.run(order=3)
    def test_delete_order(self):
        """Test case for delete_order

        Delete an order.
        """
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/orders"
        response = requests.delete(url + "/" + str(order_id))
        assert response.status_code == 200
        response = requests.delete(url + "/" + str(order_id + 1))
        assert response.status_code == 404

    @pytest.mark.run(order=4)
    def test_get_pizza_order(self):
        """Test case for get_pizza_order

        Get a pizza order given its Id. 
        """
        global order_id
        # most recent pizza order id was deleted in test above, so it will return error when queried
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/orders"
        response = requests.get(url + "/" + str(order_id))
        assert response.status_code == 404
        
        # add another pizza order to be checked below
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
        # checking most recent pizza order id should show as success
        response = requests.get(url + "/" + str(order_id))
        assert response.status_code == 200

    @pytest.mark.run(order=5)
    def test_get_pizza_count(self):
        """Test case for get_pizza_count

        Get the proper count of pizzas using a predefined algorithm. 
        """
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/orders/getcount?adult=5&child=5"
        response = requests.get(url)
        assert response.status_code == 200

    @pytest.mark.run(order=6)
    def test_add_order_pizza(self):
        """Test case for add_order_pizza

        Create a new customized pizza for a specific order given the order Id. 
        """
        global pizza_id, special_id, size_id, topping_id
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/pizza_specials"
        data = {
            "base_price": 4.99,
            "description": "So cheesy!",
            "gluten_free": True,
            "name": "Royal Cheese pizza",
            "pizza_specials_id": 123
            }
        response = requests.post(url, json=data)
        result = response.json()
        special_id = result['pizza_specials_id']
        assert response.status_code == 200
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/sizes"
        data = {"measurement": 9, "name": "medium", "pizza_sizes_id": 1, "size_price": 5}
        response = requests.post(url, json=data)
        result = response.json()
        size_id = result['pizza_sizes_id']
        assert response.status_code == 200
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/toppings"
        data = {"gluten_free": True, "name": "cheese", "pizza_toppings_id": 123, "topping_price": 2.99}
        response = requests.post(url, json=data)
        result = response.json()
        topping_id = result['pizza_toppings_id']
        assert response.status_code == 200
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/orders"
        data = {
            "count": 2,
            "pizza_size_id": size_id,
            "pizza_special_id": special_id,
            "pizza_toppings_id": [topping_id],
            "pizzas_id": 123,
            "total_price": 13
            }
        response = requests.post(url + "/" + str(order_id) + '/pizzas', json=data)
        assert response.status_code == 200
        result = response.json()
        pizza_id = result['pizzas_id']
        response = requests.post(url + "/" + str(order_id + 1) + '/pizzas', json=data)
        result = response.json()
        assert response.status_code == 404

    @pytest.mark.run(order=7)
    def test_delete_pizza_in_orders(self):
        """Test case for delete_pizza_in_orders

        Delete a pizza in order.
        """
        url = 'https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/orders/'
        response = requests.delete(url + str(order_id + 1) + '/pizza/' + str(pizza_id))
        assert response.status_code == 404
        response = requests.delete(url + str(order_id) + '/pizza/' + str(pizza_id + 1))
        assert response.status_code == 404
        response = requests.delete(url + str(order_id + 1) + '/pizza/' + str(pizza_id + 1))
        assert response.status_code == 404
        response = requests.delete(url + str(order_id) + '/pizza/' + str(pizza_id))
        assert response.status_code == 200
        response = requests.delete(url + str(order_id) + '/pizza/' + str(pizza_id))
        assert response.status_code == 404

    @pytest.mark.run(order=8)    
    def test_get_order_pizzas(self):
        """Test case for get_order_pizzas

        Get all customized pizzas for the order given the order Id.
        """
        global pizza_id
        url = 'https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/orders/'
        response = requests.get(url + str(order_id) + '/pizzas/' + str(pizza_id))
        assert response.status_code == 404
        data = {
            "count": 1,
            "pizza_size_id": size_id,
            "pizza_special_id": special_id,
            "pizza_toppings_id": [topping_id],
            "pizzas_id": 20,
            "total_price": 20
            }
        response = requests.post(url + str(order_id) + '/pizzas', json=data)
        result = response.json()
        pizza_id = result['pizzas_id']
        assert response.status_code == 200
        response = requests.get(url + str(order_id) + '/pizza/' + str(pizza_id))
        assert response.status_code == 200
        response = requests.get(url + str(order_id + 1) + '/pizza/' + str(pizza_id))
        assert response.status_code == 404
        response = requests.get(url + str(order_id) + '/pizza/' + str(pizza_id + 1))
        assert response.status_code == 404
        response = requests.get(url + str(order_id + 1) + '/pizza/' + str(pizza_id + 1))
        assert response.status_code == 404
   
    @pytest.mark.run(order=9)    
    def test_update_pizza_in_orders(self):
        """Test case for update_pizza_in_orders

        Update a specific pizza in a specific Order.
        """
        url = 'https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/orders/'
        data = {
            "count": 2,
            "pizza_size_id": size_id,
            "pizza_special_id": special_id,
            "pizza_toppings_id": [topping_id],
            "pizzas_id": 123,
            "total_price": 13
            }
        response = requests.put(url + str(order_id + 1) + '/pizza/' + str(pizza_id), json=data)
        assert response.status_code == 404
        response = requests.put(url + str(order_id) + '/pizza/' + str(pizza_id + 1), json=data)
        assert response.status_code == 404
        response = requests.put(url + str(order_id + 1) + '/pizza/' + str(pizza_id + 1), json=data)
        assert response.status_code == 404
        response = requests.put(url + str(order_id) + '/pizza/' + str(pizza_id), json=data)
        assert response.status_code == 200
        response = requests.delete(url + str(order_id) + '/pizza/' + str(pizza_id))
        assert response.status_code == 200
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/pizza_specials"
        response = requests.delete(url + "/" + str(special_id))
        assert response.status_code == 200
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/sizes"
        response = requests.delete(url + "/" + str(size_id))
        assert response.status_code == 200
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/toppings"
        response = requests.delete(url + "/" + str(topping_id))
        assert response.status_code == 200
