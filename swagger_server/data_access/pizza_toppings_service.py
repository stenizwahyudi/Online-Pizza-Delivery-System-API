# Standard library imports
import json
import os

# Local application imports
from ..database import PizzaToppingModel, db

def get_all_pizza_toppings_from_db():
    return PizzaToppingModel.query.all()

def get_pizza_topping_by_id(id):
    return PizzaToppingModel.query.get(id)

def create_pizza_topping(body):
    data = PizzaToppingModel(body.name, body.topping_price, body.gluten_free)
    db.session.add(data)
    db.session.commit()
    return data

def update_pizza_topping_by_id(id, body):
    target = db.session.query(PizzaToppingModel).get(id)
    if not target:
        return target
    new_attrs = {
        "name": body.name, 
        "topping_price": body.topping_price, 
        "gluten_free": body.gluten_free
    }
    for k, v in new_attrs.items():
        setattr(target, k, v)
    db.session.commit()
    db.session.flush()

    return target

def delete_pizza_topping_by_id(id):
    target = PizzaToppingModel.query.get(id)
    if not target:
        return target
    db.session.delete(target)
    db.session.commit()
    return target

