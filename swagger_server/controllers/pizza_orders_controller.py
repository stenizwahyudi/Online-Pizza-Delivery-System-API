# standard lib imports
import math

# third party lib imports
import connexion
import six

# external package lib imports
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.order import Order  # noqa: E501
from swagger_server.models.pizza import Pizza  # noqa: E501
from swagger_server import util
from ..data_access import pizzas_service
from ..data_access import pizza_orders_service
from ..data_access import pizza_specials_service, pizza_toppings_service, pizza_sizes_service


def add_order_pizza(body, pizza_order_id):  # noqa: E501
    """Create a new customized pizza for a specific order given the order Id. 

    Make a new customized pizza object with unique pizza id, pizza_special_id, an array of pizza_toppings_id, count, total_price and pizza_size_id to the server. Return newly added customized pizza object if succeeds posting, otherwise return with error code.  # noqa: E501

    :param body: Pizza object that needs to be stored in database
    :type body: dict | bytes
    :param pizza_order_id: The Id of the order to be queried. 
    :type pizza_order_id: int

    :rtype: Pizza
    """
    if connexion.request.is_json:
        body = Pizza.from_dict(connexion.request.get_json())  # noqa: E501
    
    # first check if order of given id exists or not
    found_order = pizza_orders_service.get_order_by_id(pizza_order_id)
    if not found_order:
        return {"error": "order by id: {} not found!".format(pizza_order_id)}, 404
    # then check if all attributes values of the given pizza all valid
    if not pizza_specials_service.get_pizza_special_by_id(body.pizza_special_id):
        return {"error": "pizza special by id: {} not found!".format(body.pizza_special_id)}, 404
    if not pizza_sizes_service.get_pizza_size_by_id(body.pizza_size_id):
        return {"error": "pizza size by id: {} not found!".format(body.pizza_size_id)}, 404
    for topping_id in body.pizza_toppings_id:
        if not pizza_toppings_service.get_pizza_topping_by_id(topping_id):
            return {"error": "pizza topping by id: {} not found!".format(topping_id)}, 404
    # then post the new pizza onto database and create Pizza object to return 
    new_pizza = pizzas_service.create_pizza(body)
    posted_new_pizza = Pizza(
        new_pizza.pizza_id,
        new_pizza.pizza_specials_id,
        new_pizza.pizza_toppings_id,
        new_pizza.pizza_sizes_id, 
        new_pizza.pizza_count,
        new_pizza.pizza_totalprice
    )
    # then add new pizza id to the current pizza id list of the order
    new_pizza_id_list = list(found_order.pizza_id)
    new_pizza_id_list.append(new_pizza.pizza_id)
    new_pizza_id_list.sort()
    # then update the order total price
    new_order_total_price = found_order.order_totalprice + new_pizza.pizza_totalprice
    # then update the order on the database
    new_order = Order(found_order.order_id,
                     found_order.pizza_stores_id, 
                     new_pizza_id_list, 
                     new_order_total_price)
    update_order = pizza_orders_service.update_order_by_id(pizza_order_id, new_order)
    return posted_new_pizza, 200
    


def add_pizza_order(body):  # noqa: E501
    """Create a new pizza order.

    Make a new pizza order object with unique pizza order id, total_price,
        an empty array of pizzas_id and pizza_store_id, and post it to the server. Return
        newly added pizza order object if succeeds posting, otherwise return with
        error code. When creating a new order, the pizza id list is by default empty list,
        since pizzas will be created after the initialization of the order and then all 
        pizza ids will be filled in the id list of this order. Please ignore the pizza id
        list in the example response. Also the total price will be 0 by default for the 
        same reason.   # noqa: E501

    :param body: Order object that needs to be stored in database
    :type body: dict | bytes

    :rtype: Order
    """
    if connexion.request.is_json:
        body = Order.from_dict(connexion.request.get_json())  # noqa: E501
    
    data = pizza_orders_service.create_order(body)

    new = Order(data.order_id,
                     data.pizza_stores_id, 
                     data.pizza_id, 
                     data.order_totalprice)
    return new, 200


def delete_order(pizza_order_id):  # noqa: E501
    """Delete an order.

    Delete an order object with unique pizza order id, order price
        and post it to the server. Return deleted pizza order object if succeeds,
        otherwise return with error code. All pizzas associated to this order will 
        also be deleted since all pizzas created for this order are unique.  # noqa: E501

    :param pizza_order_id: The Id of the order to be queried. 
    :type pizza_order_id: int

    :rtype: Order
    """
    found_order = pizza_orders_service.get_order_by_id(pizza_order_id)
    if not found_order:
        return {"error": "order not found for the given id!"}, 404
    # check if all pizza ids are valid, if not, then return error and stop deletion
    for pizza_id in found_order.pizza_id:
        found_pizza = pizzas_service.get_pizza_by_id(pizza_id)
        if not found_pizza:
            error_message = "pizza with id: {} not found!".format(pizza_id) 
            return {"error": error_message}, 404
    # now all pizza ids are valid, then delete all the pizzas first
    for pizza_id in found_order.pizza_id:
        deleted_pizza = pizzas_service.delete_pizza_by_id(pizza_id)
    # then delete the order
    deleted_order = pizza_orders_service.delete_order_by_id(pizza_order_id)
    new = Order(deleted_order.order_id,
                     deleted_order.pizza_stores_id, 
                     deleted_order.pizza_id, 
                     deleted_order.order_totalprice)
    return new, 200


def delete_pizza_in_orders(pizza_order_id, pizza_id):  # noqa: E501
    """Delete a pizza in order.

    Delete a pizza in order object from the server. Return deleted pizza object if succeeds, otherwise return with error code.  # noqa: E501

    :param pizza_order_id: The Id of the order to be queried. 
    :type pizza_order_id: int
    :param pizza_id: The Id of the customized pizza to be queried. 
    :type pizza_id: int

    :rtype: Pizza
    """
    # validate on pizza_order_id and pizza_id
    found_order = pizza_orders_service.get_order_by_id(pizza_order_id)
    if not found_order:
        return {"error": "order by id: {} not found!".format(pizza_order_id)}, 404
    
    if pizza_id not in found_order.pizza_id:
        return {"error": "pizza id: {} not in the pizza ids list of order id: {}".format(pizza_id, pizza_order_id)}, 404

    found_pizza = pizzas_service.get_pizza_by_id(pizza_id)
    if not found_pizza:
        return {"error": "pizza by id: {} not found!".format(pizza_id)}, 404

    # then delete the pizza from db
    deleted_pizza = pizzas_service.delete_pizza_by_id(pizza_id)
    pizza = Pizza(
        deleted_pizza.pizza_id,
        deleted_pizza.pizza_specials_id,
        deleted_pizza.pizza_toppings_id,
        deleted_pizza.pizza_sizes_id,
        deleted_pizza.pizza_count,
        deleted_pizza.pizza_totalprice
    )

    # then update the total price of the order and update order on db
    # also delete the pizza id from ids list in the order
    new_order_total_price = found_order.order_totalprice - deleted_pizza.pizza_totalprice
    new_pizza_id_list = list(found_order.pizza_id)
    new_pizza_id_list.remove(pizza_id)
    new_order = Order(
        found_order.order_id,
        found_order.pizza_stores_id, 
        new_pizza_id_list, 
        new_order_total_price
    )
    updated_order = pizza_orders_service.update_order_by_id(pizza_order_id, new_order)

    # return the updated pizza and code
    return pizza, 200

def get_pizza_in_orders(pizza_order_id, pizza_id):  # noqa: E501
    """Get a pizza in order.

    Get the information from a pizza that is available in an Order. Return the queried pizza object.  # noqa: E501

    :param pizza_order_id: The Id of the order to be queried. 
    :type pizza_order_id: int
    :param pizza_id: The Id of the customized pizza to be queried. 
    :type pizza_id: int

    :rtype: Pizza
    """
    found_order = pizza_orders_service.get_order_by_id(pizza_order_id)
    if not found_order:
        return {"error": "order by id: {} not found!".format(pizza_order_id)}, 404
    
    if pizza_id not in found_order.pizza_id:
        return {"error": "pizza id: {} not in the pizza ids list of order id: {}".format(pizza_id, pizza_order_id)}, 404

    found_pizza = pizzas_service.get_pizza_by_id(pizza_id)
    if not found_pizza:
        return {"error": "pizza by id: {} not found!".format(pizza_id)}, 404
    pizza = Pizza(
        found_pizza.pizza_id,
        found_pizza.pizza_specials_id,
        found_pizza.pizza_toppings_id,
        found_pizza.pizza_sizes_id,
        found_pizza.pizza_count,
        found_pizza.pizza_totalprice
    )
    return pizza, 200


def get_order_pizzas(pizza_order_id):  # noqa: E501
    """Get all customized pizzas for the order given the order Id.

    Access to all customized pizzas a customer has placed in the order by the order Id. This will return a JSON object, which is an array of Pizzas object. Successful return will give 200 status code, otherwise will give error code with error message.  # noqa: E501

    :param pizza_order_id: The Id of the order to be queried. 
    :type pizza_order_id: int

    :rtype: List[Pizza]
    """
    found_order = pizza_orders_service.get_order_by_id(pizza_order_id)
    if not found_order:
        return {"error": "order by id: {} not found!".format(pizza_order_id)}, 404
    
    pizzas = list()
    for pizza_id in found_order.pizza_id:
        found_pizza = pizzas_service.get_pizza_by_id(pizza_id)
        if not found_pizza:
            return {"error": "pizza by id: {} not found!".format(pizza_id)}, 404
        pizza = Pizza(
            found_pizza.pizza_id,
            found_pizza.pizza_specials_id,
            found_pizza.pizza_toppings_id,
            found_pizza.pizza_sizes_id,
            found_pizza.pizza_count,
            found_pizza.pizza_totalprice
        )
        pizzas.append(pizza)
    return pizzas, 200


def get_pizza_count(adult, child):  # noqa: E501
    """Get the proper count of pizzas using a predefined algorithm. 

    User will input the number of adults and number of children for the order. Both numbers are required. This will return the suggested number of pizzas to order basing on a predefined algorithm.  # noqa: E501

    :param adult: The number of adults for this order. 
    :type adult: int
    :param child: The number of children for this order. 
    :type child: int

    :rtype: InlineResponse200
    """
    size_dict = {}
    total_adult = adult + (child/1.5) # convert all to adults
    x = total_adult/3 # calculate large pizza needed
    y = math.floor(x) # the number of large pizza needed
    size_dict["large"] = y
    z = x - y # calculate the remaining pizza needed
    x = 1.3 * z # convert to medium pizzas
    y = math.floor(x) # the number of medium pizza needed
    size_dict["medium"] = y
    z = x - y # calculate the remaining pizza needed
    x = 1.438 * z # convert to small pizzas
    y = math.ceil(x) # the number of small pizza needed
    size_dict["small"] = y

    return size_dict


def get_pizza_order(pizza_order_id):  # noqa: E501
    """Get a pizza order given its Id. 

    Access to a pizza order with unique id, total_price, an array of pizzas_id, and pizza_store_id. Return the queried pizza order object.  # noqa: E501

    :param pizza_order_id: The Id of the order to be queried. 
    :type pizza_order_id: int

    :rtype: Order
    """
    found = pizza_orders_service.get_order_by_id(pizza_order_id)
    if not found:
        return {"error": "pizza order not found for the given id!"}, 404
    new = Order(
        found.order_id,
        found.pizza_stores_id, 
        found.pizza_id, 
        found.order_totalprice)
    return new, 200


def get_pizza_orders():  # noqa: E501
    """Get all pizza orders stored on the database.

    Access to all pizza orders in the database. This will return an array of pizza orders objects, including each pizza order&#x27;s unique id, total_price, an array of pizza_id, and pizza_store_id associated with this order.  # noqa: E501


    :rtype: List[Order]
    """
    data = pizza_orders_service.get_all_orders_from_db()
    pizza_orders = list()
    for item in data:
        current = Order(item.order_id,
                     item.pizza_stores_id, 
                     item.pizza_id, 
                     item.order_totalprice)
        pizza_orders.append(current)
    return pizza_orders, 200


def update_pizza_in_orders(body, pizza_order_id, pizza_id):  # noqa: E501
    """Update a specific pizza in a specific Order.

    Update a pizza that is available in an Order.  All pizza orders will include the unique order id as an integer, the order price as float, unique pizza store id and unique pizza ids. Order will offer other CRUD operations as well. Return the updated pizza object.  # noqa: E501

    :param body: Pizza object that needs to be stored in database
    :type body: dict | bytes
    :param pizza_order_id: The Id of the order to be queried. 
    :type pizza_order_id: int
    :param pizza_id: The Id of the customized pizza to be queried. 
    :type pizza_id: int

    :rtype: Pizza
    """
    if connexion.request.is_json:
        body = Pizza.from_dict(connexion.request.get_json())  # noqa: E501

    # validate on pizza_order_id and pizza_id
    found_order = pizza_orders_service.get_order_by_id(pizza_order_id)
    if not found_order:
        return {"error": "order by id: {} not found!".format(pizza_order_id)}, 404
    
    if pizza_id not in found_order.pizza_id:
        return {"error": "pizza id: {} not in the pizza ids list of order id: {}".format(pizza_id, pizza_order_id)}, 404

    found_pizza = pizzas_service.get_pizza_by_id(pizza_id)
    if not found_pizza:
        return {"error": "pizza by id: {} not found!".format(pizza_id)}, 404

    # update pizza and initiate the return value
    updated_pizza = pizzas_service.update_pizza_by_id(pizza_id, body)
    pizza = Pizza(
        updated_pizza.pizza_id,
        updated_pizza.pizza_specials_id,
        updated_pizza.pizza_toppings_id,
        updated_pizza.pizza_sizes_id,
        updated_pizza.pizza_count,
        updated_pizza.pizza_totalprice
    )

    # update the order with new total price
    new_order_total_price = found_order.order_totalprice - found_pizza.pizza_totalprice + updated_pizza.pizza_totalprice
    new_order = Order(
        found_order.order_id,
        found_order.pizza_stores_id, 
        found_order.pizza_id, 
        new_order_total_price
    )
    updated_order = pizza_orders_service.update_order_by_id(pizza_order_id, new_order)
    
    # return the updated pizza and code
    return pizza, 200

