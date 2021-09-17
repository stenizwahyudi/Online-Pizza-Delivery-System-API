# coding: utf-8

from __future__ import absolute_import

import requests

from flask import json
from six import BytesIO

from swagger_server.models.pizza_size import PizzaSize  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPizzaSizesController(BaseTestCase):
    """PizzaSizesController integration test stubs"""

    latest_id = 0

    def test_add_pizza_size(self):
        """Test case for add_pizza_size

        Create a new pizza size.
        """
        global latest_id
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/sizes"
        data = {"measurement": 9, "name": "medium", "pizza_sizes_id": 1, "size_price": 5}
        response = requests.post(url, json=data)
        result = response.json()
        latest_id = result['pizza_sizes_id']
        assert response.status_code == 200

    def test_get_pizza_sizes(self):
        """Test case for get_pizza_toppings

        Get all available pizza sizes. 
        """
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/sizes"
        response = requests.get(url)
        assert response.status_code == 200


    def test_delete_pizza_size(self):
        """Test case for delete_pizza_size

        Delete a pizza size given its Id. 
        """
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/sizes"
        response = requests.delete(url + "/" + str(latest_id))
        assert response.status_code == 200
        response = requests.delete(url + "/" + str(latest_id + 1))
        assert response.status_code == 404

    def test_get_pizza_size(self):
        """Test case for get_pizza_size

        Get a pizza size given its Id. 
        """
        global latest_id
        # most recent pizza size id was deleted in test above, so it will return error when queried
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/sizes"
        response = requests.get(url + "/" + str(latest_id))
        assert response.status_code == 404
        # add another pizza size to be checked below
        data = {"measurement": 9, "name": "medium", "pizza_sizes_id": 1, "size_price": 5}
        response = requests.post(url, json=data)
        result = response.json()
        latest_id = result['pizza_sizes_id']
        # checking most recent pizza size id should show as success
        response = requests.get(url + "/" + str(latest_id))
        assert response.status_code == 200


    def test_update_pizza_size(self):
        """Test case for update_pizza_size

        Update a new pizza size given its Id. 
        """
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/sizes"
        data = {"measurement": 20, "name": "small", "pizza_sizes_id": 1, "size_price": 9.99}
        response = requests.put(url + "/" + str(latest_id), json=data)
        assert response.status_code == 200
        response = requests.put(url + "/" + str(latest_id + 1), json=data)
        assert response.status_code == 404
        response = requests.delete(url + "/" + str(latest_id))
        assert response.status_code == 200
