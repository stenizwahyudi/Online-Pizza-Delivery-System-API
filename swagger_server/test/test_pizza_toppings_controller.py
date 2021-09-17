# coding: utf-8

from __future__ import absolute_import

import requests

from flask import json
from six import BytesIO

from swagger_server.models.pizza_topping import PizzaTopping  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPizzaToppingsController(BaseTestCase):
    """PizzaToppingsController integration test stubs"""

    latest_id = 0

    def test_add_pizza_topping(self):
        """Test case for add_pizza_topping

        Create a new pizza topping. 
        """
        global latest_id
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/toppings"
        data = {"gluten_free": True, "name": "cheese", "pizza_toppings_id": 123, "topping_price": 2.99}
        response = requests.post(url, json=data)
        result = response.json()
        latest_id = result['pizza_toppings_id']
        assert response.status_code == 200

    def test_get_pizza_toppings(self):
        """Test case for get_pizza_toppings

        Get all available pizza toppings. 
        """
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/toppings"
        response = requests.get(url)
        assert response.status_code == 200

    def test_delete_pizza_topping(self):
        """Test case for delete_pizza_topping

        Delete the pizza topping given Id. 
        """
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/toppings"
        response = requests.delete(url + "/" + str(latest_id))
        assert response.status_code == 200
        response = requests.delete(url + "/" + str(latest_id + 1))
        assert response.status_code == 404

    def test_get_pizza_topping(self):
        """Test case for get_pizza_topping

        Get the pizza topping given Id. 
        """
        global latest_id
        # most recent pizza topping id was deleted in test above, so it will return error when queried
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/toppings"
        response = requests.get(url + "/" + str(latest_id))
        assert response.status_code == 404
        # add another pizza topping to be checked below
        data = {"gluten_free": True, "name": "cheese", "pizza_toppings_id": 123, "topping_price": 2.99}
        response = requests.post(url, json=data)
        result = response.json()
        latest_id = result['pizza_toppings_id']
        # checking most recent pizza topping id should show as success
        response = requests.get(url + "/" + str(latest_id))
        assert response.status_code == 200


    def test_update_pizza_topping(self):
        """Test case for update_pizza_topping

        Update the pizza topping given Id. 
        """
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/toppings"
        data = {"gluten_free": False, "name": "cheese", "pizza_toppings_id": 123, "topping_price": 1.99}
        response = requests.put(url + "/" + str(latest_id), json=data)
        assert response.status_code == 200
        response = requests.put(url + "/" + str(latest_id + 1), json=data)
        assert response.status_code == 404
        response = requests.delete(url + "/" + str(latest_id))
        assert response.status_code == 200
