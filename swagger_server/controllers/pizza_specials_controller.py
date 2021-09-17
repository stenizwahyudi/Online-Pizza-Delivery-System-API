import connexion
import six

from swagger_server.models.pizza_special import PizzaSpecial  # noqa: E501
from swagger_server import util

from ..data_access import pizza_specials_service

def add_pizza_special(body):  # noqa: E501
    """Create a new pizza special. 

    Make a new pizza special object with unique pizza special id, name, description, base price, and gluten_free boolean value, and post it to the server. Return newly added pizza special object if succeeds posting, otherwise return with error code and error message.  # noqa: E501

    :param body: PizzaSpecial object that needs to be stored in database
    :type body: dict | bytes

    :rtype: PizzaSpecial
    """
    if connexion.request.is_json:
        body = PizzaSpecial.from_dict(connexion.request.get_json())  # noqa: E501

    data = pizza_specials_service.create_pizza_special(body)
    new = PizzaSpecial(data.pizza_specials_id,
                    data.specials_name, 
                    data.specials_description, 
                    data.specials_baseprice,
                    data.specials_glutenfree)
    return new, 200


def delete_pizza_special(pizza_special_id):  # noqa: E501
    """Delete a pizza special given its Id. 

    Given the pizza special Id, delete this pizza special completely from the server. Return the deleted pizza special object.  # noqa: E501

    :param pizza_special_id: The Id of the queried pizza special. 
    :type pizza_special_id: int

    :rtype: PizzaSpecial
    """
    data = pizza_specials_service.delete_pizza_special_by_id(pizza_special_id)
    if not data:
        return {}, 404
    deleted = PizzaSpecial(data.pizza_specials_id,
                        data.specials_name, 
                    data.specials_description, 
                    data.specials_baseprice,
                    data.specials_glutenfree)
    return deleted, 200


def get_pizza_special(pizza_special_id):  # noqa: E501
    """Get a pizza special given its Id. 

    Access to the information of a pizza special object by its ID, including the unique pizza special ID, name, description, base_price and gluten_free. This will return a JSON object after a successful calling, otherwise error code with error message.  # noqa: E501

    :param pizza_special_id: The Id of the queried pizza special. 
    :type pizza_special_id: int

    :rtype: PizzaSpecial
    """
    data = pizza_specials_service.get_pizza_special_by_id(pizza_special_id)
    if not data:
        return {}, 404
    else:
        found = PizzaSpecial(data.pizza_specials_id, 
                            data.specials_name, 
                    data.specials_description, 
                    data.specials_baseprice,
                    data.specials_glutenfree)
    return found, 200


def get_pizza_specials():  # noqa: E501
    """Get all available pizza specials from the database. 

    Get all the pizza special objects stored on the database. This will return an array of JSON objects that represent the pizza specials. Each object will contain the information including pizza_specials_id as an integer, name and description as string, base price of the special as a float number, and the boolean value for gluten_free.  # noqa: E501


    :rtype: List[PizzaSpecial]
    """
    got_data = pizza_specials_service.get_all_pizza_specials_from_db()
    pizza_specials = []
    for data in got_data:
        current = PizzaSpecial(data.pizza_specials_id, 
                            data.specials_name, 
                    data.specials_description, 
                    data.specials_baseprice,
                    data.specials_glutenfree)
        pizza_specials.append(current)
    return pizza_specials, 200


def update_pizza_special(body, pizza_special_id):  # noqa: E501
    """Update a pizza special given its Id and new content. 

    Update the pizza special. Cannot update Id since it is unique to the pizza special. But can update name, description, base_price and gluten_free. Return the updated pizza special object.  # noqa: E501

    :param body: PizzaSpecial object that needs to be stored in database
    :type body: dict | bytes
    :param pizza_special_id: The Id of the queried pizza special. 
    :type pizza_special_id: int

    :rtype: PizzaSpecial
    """
    if connexion.request.is_json:
        body = PizzaSpecial.from_dict(connexion.request.get_json())  # noqa: E501
    data = pizza_specials_service.update_pizza_special_by_id(pizza_special_id, body)
    if not data:
        return {}, 404
    new = PizzaSpecial(data.pizza_specials_id,
                    data.specials_name, 
                    data.specials_description, 
                    data.specials_baseprice,
                    data.specials_glutenfree)
    return new, 200
