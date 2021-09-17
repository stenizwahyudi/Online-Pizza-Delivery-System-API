import connexion
import six

from swagger_server.models.pizza_size import PizzaSize  # noqa: E501
from swagger_server import util

from ..data_access import pizza_sizes_service


def add_pizza_size(body):  # noqa: E501
    """Create a new pizza size.

    Make a new pizza size object with unique pizza size id, size name, size measurement and size price, and post it to the server. Return newly added pizza size object if succeeds posting, otherwise return with error code.  # noqa: E501

    :param body: PizzaSize object that needs to be stored in database
    :type body: dict | bytes

    :rtype: PizzaSize
    """
    if connexion.request.is_json:
        body = PizzaSize.from_dict(connexion.request.get_json())  # noqa: E501
    
    data = pizza_sizes_service.create_pizza_size(body)
    new = PizzaSize(data.pizza_sizes_id,
                    data.name, 
                    data.measurement, 
                    data.size_price)
    return new, 200


def delete_pizza_size(pizza_size_id):  # noqa: E501
    """Delete a pizza size given its Id. 

    Given the pizza size Id, delete this pizza size completely from the server. Return the deleted pizza size object.  # noqa: E501

    :param pizza_size_id: The Id of the pizza size to be queried. 
    :type pizza_size_id: int

    :rtype: PizzaSize
    """
    data = pizza_sizes_service.delete_pizza_size_by_id(pizza_size_id)
    if not data:
        return {}, 404
    deleted = PizzaSize(data.pizza_sizes_id,
                        data.name, 
                        data.measurement, 
                        data.size_price)
    return deleted, 200


def get_pizza_size(pizza_size_id):  # noqa: E501
    """Get a pizza size given its Id. 

    Access to a pizza size with unique id, name, measurement in inches as a float number, and price as float number. Return the queried pizza size object.  # noqa: E501

    :param pizza_size_id: The Id of the pizza size to be queried. 
    :type pizza_size_id: int

    :rtype: PizzaSize
    """
    item = pizza_sizes_service.get_pizza_size_by_id(pizza_size_id)
    if not item:
        return {}, 404
    else:
        found = PizzaSize(item.pizza_sizes_id, 
                            item.name,
                            item.measurement,
                            item.size_price)
        return found, 200


def get_pizza_sizes():  # noqa: E501
    """Get all available pizza sizes.

    Access to all pizza sizes we provide. All pizza sizes will include the unique size id as an interger, the size name as a string, size measurement as a float number and the price for the size as a float number. Sizes will, by default, include &#x60;small&#x60;, &#x60;medium&#x60; and &#x60;large&#x60;, but will offer other CRUD operations as well. Return all pizza sizes object array.  # noqa: E501


    :rtype: List[PizzaSize]
    """
    data = pizza_sizes_service.get_all_pizza_sizes_from_db()
    pizza_sizes = list()
    for item in data:
        current = PizzaSize(item.pizza_sizes_id, 
                            item.name,
                            item.measurement,
                            item.size_price)
        pizza_sizes.append(current)
    return pizza_sizes, 200


def update_pizza_size(body, pizza_size_id):  # noqa: E501
    """Update a new pizza size given its Id. 

    Update the pizza size. Cannot update Id since it is unique to the pizza size. But can update size name, size measurement, or size price. Return the updated pizza size object.  # noqa: E501

    :param body: PizzaSize object that needs to be stored in database
    :type body: dict | bytes
    :param pizza_size_id: The Id of the pizza size to be queried. 
    :type pizza_size_id: int

    :rtype: PizzaSize
    """
    if connexion.request.is_json:
        body = PizzaSize.from_dict(connexion.request.get_json())  # noqa: E501
    data = pizza_sizes_service.update_pizza_size_by_id(pizza_size_id, body)
    if not data:
        return {}, 404
    new = PizzaSize(data.pizza_sizes_id,
                    data.name, 
                    data.measurement, 
                    data.size_price)
    return new, 200
        
