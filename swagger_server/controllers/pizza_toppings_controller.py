import connexion
import six

from swagger_server.models.pizza_topping import PizzaTopping  # noqa: E501
from swagger_server import util

from ..data_access import pizza_toppings_service


def add_pizza_topping(body):  # noqa: E501
    """Create a new pizza topping. 

    Make a new pizza topping with new unique Id, new name, new price, and new gluten_free property and store onto the database. Return newly created pizza topping object.  # noqa: E501

    :param body: PizzaTopping object that needs to be stored in database
    :type body: dict | bytes

    :rtype: PizzaTopping
    """
    if connexion.request.is_json:
        body = PizzaTopping.from_dict(connexion.request.get_json())  # noqa: E501
    
    data = pizza_toppings_service.create_pizza_topping(body)
    new = PizzaTopping(data.pizza_toppings_id,
                       data.name, 
                       data.topping_price, 
                       data.gluten_free)
    return new, 200


def delete_pizza_topping(pizza_topping_id):  # noqa: E501
    """Delete the pizza topping given Id. 

    Delete the pizza topping with the given Id. Return the deleted pizza topping object.  # noqa: E501

    :param pizza_topping_id: The Id of the pizza topping to be queried. 
    :type pizza_topping_id: int

    :rtype: PizzaTopping
    """
    data = pizza_toppings_service.delete_pizza_topping_by_id(pizza_topping_id)
    if not data:
        return {}, 404
    deleted = PizzaTopping(data.pizza_toppings_id,
                           data.name, 
                           data.topping_price, 
                           data.gluten_free)
    return deleted, 200


def get_pizza_topping(pizza_topping_id):  # noqa: E501
    """Get the pizza topping given Id. 

    Get the pizza topping with the given Id. Return the queried pizza topping object.  # noqa: E501

    :param pizza_topping_id: The Id of the pizza topping to be queried. 
    :type pizza_topping_id: int

    :rtype: PizzaTopping
    """
    item = pizza_toppings_service.get_pizza_topping_by_id(pizza_topping_id)
    if not item:
        return {}, 404
    else:
        found = PizzaTopping(item.pizza_toppings_id, 
                             item.name,
                             item.topping_price,
                             item.gluten_free)
        return found, 200


def get_pizza_toppings():  # noqa: E501
    """Get all available pizza toppings. 

    Get access to all pizza toppings stored in the database. By default, some toppings are already available on start and provided by the vendor. All pizza toppings will include its Id as an integer, name as a string, price as a float number, and gluten free or not as a boolean value. Return all pizza toppings objects in an array.  # noqa: E501


    :rtype: List[PizzaTopping]
    """
    data = pizza_toppings_service.get_all_pizza_toppings_from_db()
    pizza_toppings = list()
    for item in data:
        current = PizzaTopping(item.pizza_toppings_id, 
                            item.name,
                            item.topping_price,
                            item.gluten_free)
        pizza_toppings.append(current)
    return pizza_toppings, 200


def update_pizza_topping(body, pizza_topping_id):  # noqa: E501
    """Update the pizza topping given Id. 

    Update the pizza topping with the given Id. Cannot update the pizza_toppings_id since it is unique, but can update name, price, or gluten_free.  Return the updated pizza topping object.  # noqa: E501

    :param body: PizzaTopping object that needs to be stored in database
    :type body: dict | bytes
    :param pizza_topping_id: The Id of the pizza topping to be queried. 
    :type pizza_topping_id: int

    :rtype: PizzaTopping
    """
    if connexion.request.is_json:
        body = PizzaTopping.from_dict(connexion.request.get_json())  # noqa: E501
    
    data = pizza_toppings_service.update_pizza_topping_by_id(pizza_topping_id, body)
    if not data:
        return {}, 404
    new = PizzaTopping(data.pizza_toppings_id,
                       data.name, 
                       data.topping_price, 
                       data.gluten_free)
    return new, 200
