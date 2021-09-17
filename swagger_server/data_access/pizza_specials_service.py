# Standard library imports
import json
import os

# Local application imports
from ..database import PizzaSpecialModel, db

# SAMPLE_PATH = "data_samples/sample_pizza_specials.json"

def get_all_pizza_specials_from_db():
    return PizzaSpecialModel.query.all()

def get_pizza_special_by_id(id):
    return PizzaSpecialModel.query.get(id)

def create_pizza_special(body):
    # data = PizzaSpecialModel(body.name, body.description, body.baseprice, body.glutenfree)
    data = PizzaSpecialModel(body.name, body.description, body.base_price, body.gluten_free)
    db.session.add(data)
    db.session.commit()
    return data

def update_pizza_special_by_id(id, body):
    target = db.session.query(PizzaSpecialModel).get(id)
    if not target:
        return target
    new_attrs = {
        "specials_name": body.name, 
        "specials_description": body.description, 
        "specials_baseprice": body.base_price,
        "specials_glutenfree": body.gluten_free
    }
    for k, v in new_attrs.items():
        setattr(target, k, v)
    db.session.commit()
    db.session.flush()

    return target

def delete_pizza_special_by_id(id):
    target = PizzaSpecialModel.query.get(id)
    if not target:
        return target
    db.session.delete(target)
    db.session.commit()
    return target
