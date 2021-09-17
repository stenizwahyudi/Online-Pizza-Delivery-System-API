# Standard library imports
import json
import os

# Local application imports
from ..database import PizzaModel, db
from .pizza_sizes_service import get_pizza_size_by_id
from .pizza_specials_service import get_pizza_special_by_id
from .pizza_toppings_service import get_pizza_topping_by_id

def get_all_pizzas_from_db():
    return PizzaModel.query.all()

def get_pizza_by_id(id):
    return PizzaModel.query.get(id)

def create_pizza(body):
    # first get the total price for this new pizza
    # manually set total price will not work
    total_price = get_total_price_for_pizza(body)
    data = PizzaModel(
        body.count, 
        total_price, 
        body.pizza_special_id,
        body.pizza_toppings_id,
        body.pizza_size_id)
    db.session.add(data)
    db.session.commit()
    return data

def update_pizza_by_id(id, body):
    target = db.session.query(PizzaModel).get(id)
    if not target:
        return target
    # get the new total price
    new_total_price = get_total_price_for_pizza(body)
    new_attrs = {
        "pizza_count": body.count, 
        "pizza_totalprice": new_total_price, 
        "pizza_specials_id": body.pizza_special_id,
        "pizza_toppings_id": body.pizza_toppings_id,
        "pizza_sizes_id": body.pizza_size_id
    }
    for k, v in new_attrs.items():
        setattr(target, k, v)
    db.session.commit()
    db.session.flush()

    return target

def delete_pizza_by_id(id):
    target = PizzaModel.query.get(id)
    if not target:
        return target
    db.session.delete(target)
    db.session.commit()
    return target

def get_total_price_for_pizza(pizza):
    total_price = 0
    
    # assume pizza size id is valid
    total_price += get_pizza_size_by_id(pizza.pizza_size_id).size_price
    # assume pizza special id is valid
    total_price += get_pizza_special_by_id(pizza.pizza_special_id).specials_baseprice
    # assume pizza topping ids are all valid
    for topping_id in pizza.pizza_toppings_id:
        total_price += get_pizza_topping_by_id(topping_id).topping_price
    
    total_price = total_price * pizza.count
    return total_price


