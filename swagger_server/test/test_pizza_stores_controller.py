# coding: utf-8

from __future__ import absolute_import

import requests
import pytest

from flask import json
from six import BytesIO

from swagger_server.models.pizza_store import PizzaStore  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPizzaStoresController(BaseTestCase):
    """PizzaStoresController integration test stubs"""

    latest_id = 0
    spefcial_id = 0

    @pytest.mark.run(order=1)
    def test_add_pizza_stores(self):
        """Test case for add_pizza_stores

        Create a new pizza store.
        """
        global latest_id, special_id
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
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/stores"
        data = {
            "pizza_stores_id": 123,
            "specials": [special_id],
            "store_location": "225 Terry Ave, Seattle, WA 98109",
            "store_name": "Turing Pizza NEU Seattle"
            }
        response = requests.post(url, json=data)
        result = response.json()
        latest_id = result['pizza_stores_id']
        assert response.status_code == 200

    @pytest.mark.run(order=2)
    def test_get_all_pizza_stores(self):
        """Test case for get_all_pizza_stores

        Get all available pizza stores.
        """
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/stores"
        response = requests.get(url)
        assert response.status_code == 200

    @pytest.mark.run(order=3)
    def test_delete_pizza_store(self):
        """Test case for delete_pizza_store

        Delete a pizza store given its Id. 
        """
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/stores"
        response = requests.delete(url + "/" + str(latest_id))
        assert response.status_code == 200
        response = requests.delete(url + "/" + str(latest_id + 1))
        assert response.status_code == 404

    @pytest.mark.run(order=4)
    def test_get_pizza_store(self):
        """Test case for get_pizza_store

        Delete a pizza store given its Id. 
        """
        global latest_id
        # most recent pizza store id was deleted in test above, so it will return error when queried
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/stores"
        response = requests.get(url + "/" + str(latest_id))
        assert response.status_code == 404
        # add another pizza store to be checked below
        data = {
            "pizza_stores_id": 123,
            "specials": [special_id],
            "store_location": "401 NE Northgate Way, Seattle, WA 98125",
            "store_name": "Turing Pizza Northgate Mall"
            }
        response = requests.post(url, json=data)
        result = response.json()
        latest_id = result['pizza_stores_id']
        # checking most recent pizza store id should show as success
        response = requests.get(url + "/" + str(latest_id))
        assert response.status_code == 200

    @pytest.mark.run(order=5)
    def test_update_pizza_store(self):
        """Test case for update_pizza_store

        Update a new pizza store given its Id. 
        """
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/stores"
        data = {
            "pizza_stores_id": 123,
            "specials": [special_id],
            "store_location": "401 Terry Ave, Seattle, WA 98109",
            "store_name": "Turing Pizza NEU Seattle"
            }
        response = requests.put(url + "/" + str(latest_id), json=data)
        assert response.status_code == 200
        response = requests.put(url + "/" + str(latest_id + 1), json=data)
        assert response.status_code == 404

    @pytest.mark.run(order=6)
    def test_get_pizza_store_specials(self):
        """Test case for get_pizza_store_specials

        Get a pizza store specials given its Id. 
        """
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/stores"
        response = requests.get(url + "/" + str(latest_id) + "/specials")
        assert response.status_code == 200
        response = requests.get(url + "/" + str(latest_id + 1) + "/specials")
        assert response.status_code == 404
        response = requests.get(url + "/" + str(latest_id) + "/specials")
        assert response.status_code == 200

    @pytest.mark.run(order=7)
    def test_update_pizza_store_specials(self):
        """Test case for add_pizza_store_specials & delete_pizza_store_specials

        Add or Delete pizza specials for a given store based on its ID. 
        """
        global latest_id
        url = "https://murmuring-depths-61941.herokuapp.com/TuringPizza/TuringPizza/1.0.0/stores"
        response = requests.post(url + "/" + str(latest_id) + "/specials/" + str(special_id))
        assert response.status_code == 400
        response = requests.post(url + "/" + str(latest_id + 1) + "/specials/" + str(special_id))
        assert response.status_code == 404
        response = requests.post(url + "/" + str(latest_id+ 1) + "/specials/" + str(special_id + 1))
        assert response.status_code == 404
        response = requests.delete(url + "/" + str(latest_id) + "/specials/" + str(special_id + 1))
        assert response.status_code == 404
        response = requests.delete(url + "/" + str(latest_id) + "/specials/" + str(special_id))
        assert response.status_code == 200
        response = requests.delete(url + "/" + str(latest_id) + "/specials/" + str(special_id))
        assert response.status_code == 404
        response = requests.post(url + "/" + str(latest_id) + "/specials/" + str(special_id))
        assert response.status_code == 200
        response = requests.delete(url + "/" + str(latest_id))
