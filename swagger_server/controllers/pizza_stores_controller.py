import connexion
import six

from swagger_server.models.pizza_store import PizzaStore  # noqa: E501
from swagger_server.models.pizza_special import PizzaSpecial
from swagger_server import util

from ..data_access import pizza_stores_service
from ..data_access import pizza_specials_service


def add_pizza_stores(body):  # noqa: E501
    """Create a new pizza store.
    Make a new pizza store object with unique pizza store id, store name, store location and post it to the server. Return newly added pizza store object if succeeds posting, otherwise return with error code.  # noqa: E501
    :param body: PizzaStore object that needs to be stored in database
    :type body: dict | bytes
    :rtype: PizzaStore
    """
    if connexion.request.is_json:
        body = PizzaStore.from_dict(connexion.request.get_json())  # noqa: E501
    data = pizza_stores_service.create_pizza_store(body)

    new = PizzaStore(data.pizza_stores_id,
                     data.store_name, 
                     data.store_location, 
                     data.pizza_specials_id)
    return new, 200


def delete_pizza_store(pizza_store_id):  # noqa: E501
    """Delete a pizza store given its Id. 
    Given the pizza store Id, delete this pizza store completely from the server. Return the deleted pizza store object.  # noqa: E501
    :param pizza_store_id: The Id of the pizza store to be queried. 
    :type pizza_store_id: int
    :rtype: PizzaStore
    """
    data = pizza_stores_service.delete_pizza_store_by_id(pizza_store_id)
    if not data:
        return {}, 404
    deleted = PizzaStore(data.pizza_stores_id,
                         data.store_name, 
                         data.store_location, 
                         data.pizza_specials_id)
    return deleted, 200

def get_all_pizza_stores():  # noqa: E501
	
    """
    Get all available pizza stores.
    
    Access to all pizza stores we provide. All pizza stores will include the unique store id as an interger, the store name as a string, store location as a string. Store will offer other CRUD operations as well. Return all stores  object array.  # noqa: E501
    
    :rtype: List[PizzaStore]
    """
    data = pizza_stores_service.get_all_pizza_stores_from_db()
    pizza_stores = list()
    for item in data:
        current = PizzaStore(item.pizza_stores_id, 
                             item.store_name,
                             item.store_location,
                             item.pizza_specials_id)
        pizza_stores.append(current)
    return pizza_stores, 200
    

def get_pizza_store(pizza_store_id):  # noqa: E501
    """Get a pizza store given its Id. 
    Access to a pizza store with unique id, name, location. Return the queried pizza store object.  # noqa: E501
    :param pizza_store_id: The Id of the pizza store to be queried. 
    :type pizza_store_id: int
    :rtype: PizzaStore
    """
    item = pizza_stores_service.get_pizza_store_by_id(pizza_store_id)
    if not item:
        return {}, 404
    else:
        found = PizzaStore(item.pizza_stores_id, 
                           item.store_name,
                           item.store_location,
                           item.pizza_specials_id)
        return found, 200


def get_pizza_store_specials(pizza_store_id):  # noqa: E501
    """Get a pizza store specials given its Id. 
    Access to a pizza store specials with the stores unique id. Return the queried pizza store object.  # noqa: E501
    :param pizza_store_id: The Id of the pizza store to be queried. 
    :type pizza_store_id: int
    :rtype: PizzaStore
    """
    # return 'do some magic!'
    found_store = pizza_stores_service.get_pizza_store_by_id(pizza_store_id)
    specials_list = list()
    if not found_store:
        return {}, 404
    else:
        # found = PizzaStore(item.pizza_stores_id, 
        #                     item.store_name,
        #                     item.store_location,
        #                    item.pizza_specials_id)
        # return found, 200
        for pizza_special_id in found_store.pizza_specials_id:
            found_pizza_special = pizza_specials_service.get_pizza_special_by_id(pizza_special_id)
            if not found_pizza_special:
                return {"error": "this pizza special not found!"}, 404
            found = PizzaSpecial(found_pizza_special.pizza_specials_id,
                    found_pizza_special.specials_name, 
                    found_pizza_special.specials_description, 
                    found_pizza_special.specials_baseprice,
                    found_pizza_special.specials_glutenfree)
            specials_list.append(found)
        return specials_list, 200


def update_pizza_store(body, pizza_store_id):  # noqa: E501
    """Update a new pizza store given its Id. 
    Update the pizza store. Cannot update Id since it is unique to the pizza store. But can update store name, store location. Return the updated pizza store object.  # noqa: E501
    :param body: PizzaStore object that needs to be stored in database
    :type body: dict | bytes
    :param pizza_store_id: The Id of the pizza store to be queried. 
    :type pizza_store_id: int
    :rtype: PizzaStore
    """
    if connexion.request.is_json:
        body = PizzaStore.from_dict(connexion.request.get_json())  # noqa: E501
        
    data = pizza_stores_service.update_pizza_store_by_id(pizza_store_id, body)
    if not data:
        return {}, 404
    new = PizzaStore(data.pizza_stores_id,
                     data.store_name, 
                     data.store_location,
                     data.pizza_specials_id)
    return new, 200


def delete_pizza_store_specials(pizza_store_id, pizza_special_id):  # noqa: E501
    """Delete pizza specials for a given store based on its ID. 
    Return the updated pizza store object.  # noqa: E501
    :param pizza_store_id: The Id of the pizza store to be queried. 
    :type pizza_store_id: int
    :param pizza_special_id: The Id of the queried pizza special. 
    :type pizza_special_id: int
    :rtype: PizzaStore
    """
    found_store = pizza_stores_service.get_pizza_store_by_id(pizza_store_id)
    if not found_store:
        return {"error": "store not found!"}, 404
    if pizza_special_id not in found_store.pizza_specials_id:
        return {"error": "pizza special not found for this store!"}, 404
    new_list = list(found_store.pizza_specials_id)
    new_list.remove(pizza_special_id)    
    new = PizzaStore(found_store.pizza_stores_id,
                     found_store.store_name, 
                     found_store.store_location,
                     new_list)
    pizza_stores_service.update_pizza_store_by_id(pizza_store_id, new)
    return new, 200

def add_pizza_store_specials(pizza_store_id, pizza_special_id):  # noqa: E501
    """Add a new pizza special ID for a given store based on its ID. 
    Return the updated pizza store object.  # noqa: E501
    :param pizza_store_id: The Id of the pizza store to be queried. 
    :type pizza_store_id: int
    :param pizza_special_id: The Id of the queried pizza special. 
    :type pizza_special_id: int
    :rtype: PizzaStore
    """

    found_store = pizza_stores_service.get_pizza_store_by_id(pizza_store_id)
    if not found_store:
        return {"error": "store not found!"}, 404
    if pizza_special_id in found_store.pizza_specials_id:
        return {"error": "pizza special already exists!"}, 400
    found_pizza_special = pizza_specials_service.get_pizza_special_by_id(pizza_special_id)
    if not found_pizza_special:
        return {"error": "pizza special not found!"}, 404
    new_list = list(found_store.pizza_specials_id)
    new_list.append(pizza_special_id)
    new_list = sorted(new_list)    
    new = PizzaStore(found_store.pizza_stores_id,
                     found_store.store_name, 
                     found_store.store_location,
                     new_list)
    pizza_stores_service.update_pizza_store_by_id(pizza_store_id, new)
    return new, 200