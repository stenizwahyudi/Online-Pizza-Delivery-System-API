# coding: utf-8

from __future__ import absolute_import

import requests

from flask import json
from six import BytesIO

from swagger_server.models.pizza_special import PizzaSpecial  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPizzaSpecialsController(BaseTestCase):
    """PizzaSpecialsController integration test stubs"""

    latest_id = 0

    def test_add_pizza_special(self):
        """Test case for add_pizza_special

        Create a new pizza special. 
        """
        global latest_id
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
        latest_id = result['pizza_specials_id']
        assert response.status_code == 200

    def test_get_pizza_specials(self):
        """Test case for get_pizza_specials

        Get all available pizza specials from the database. 
        """
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/pizza_specials"
        response = requests.get(url)
        assert response.status_code == 200

    def test_delete_pizza_special(self):
        """Test case for delete_pizza_special

        Delete a pizza special given its Id. 
        """
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/pizza_specials"
        response = requests.delete(url + "/" + str(latest_id))
        assert response.status_code == 200
        response = requests.delete(url + "/" + str(latest_id + 1))
        assert response.status_code == 404

    def test_get_pizza_special(self):
        """Test case for get_piza_special

        Get a pizza special given its Id. 
        """
        global latest_id
        # most recent pizza special id was deleted in test above, so it will return error when queried
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/pizza_specials"
        response = requests.get(url + "/" + str(latest_id))
        assert response.status_code == 404
        # add another pizza special to be checked below
        data = {
            "base_price": 7.99,
            "description": "Meat, meat, and ... MEAT",
            "gluten_free": True,
            "name": "Meat Lovers",
            "pizza_specials_id": 123
            }
        response = requests.post(url, json=data)
        result = response.json()
        latest_id = result['pizza_specials_id']
        # checking most recent pizza special id should show as success
        response = requests.get(url + "/" + str(latest_id))
        assert response.status_code == 200

    def test_update_pizza_special(self):
        """Test case for update_pizza_special

        Update a pizza special given its Id and new content. 
        """
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/pizza_specials"
        data = {
            "base_price": 5.99,
            "description": "Meat, meat, and ... MEAT",
            "gluten_free": True,
            "name": "Meat Lovers",
            "pizza_specials_id": 123
            }
        response = requests.put(url + "/" + str(latest_id), json=data)
        assert response.status_code == 200
        response = requests.put(url + "/" + str(latest_id + 1), json=data)
        assert response.status_code == 404
        response = requests.delete(url + "/" + str(latest_id))
        assert response.status_code == 200
