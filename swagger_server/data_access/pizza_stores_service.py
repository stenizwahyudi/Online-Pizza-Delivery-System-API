# Standard library imports
import json
import os

# Local application imports
from ..database import PizzaStoreModel, PizzaSpecialModel, db
from sqlalchemy import and_

def get_all_pizza_stores_from_db():
    return PizzaStoreModel.query.all()

def get_pizza_store_by_id(id):
    return PizzaStoreModel.query.get(id)

def create_pizza_store(body):
    data = PizzaStoreModel(body.store_name, body.store_location, body.specials)
    db.session.add(data)
    db.session.commit()
    return data

def update_pizza_store_by_id(id, body):
    target = db.session.query(PizzaStoreModel).get(id)
    if not target:
        return target
    new_attrs = {
        "store_name": body.store_name, 
        "store_location": body.store_location,
        "pizza_specials_id": body.specials
    }
    for k, v in new_attrs.items():
        setattr(target, k, v)
    db.session.commit()
    db.session.flush()

    return target

def delete_pizza_store_by_id(id):
    target = PizzaStoreModel.query.get(id)
    if not target:
        return target
    db.session.delete(target)
    db.session.commit()
    return target


def update_pizza_store_specials_by_id(id, body, sid):
    # target = db.session.query(PizzaStoreModel).join(PizzaStoreModel, PizzaStoreModel.pizza_specials_id == PizzaSpecialModel.pizza_specials_id)
    # target = db.session.query(PizzaStoreModel).join(PizzaStoreModel, and_(PizzaStoreModel.pizza_specials_id == PizzaSpecialModel.pizza_specials_id, PizzaSpecialModel.pizza_specials_id.in_(sid)))
    
    target = db.session.query(PizzaStoreModel).join(PizzaSpecialModel, and_(PizzaStoreModel.pizza_specials_id == PizzaSpecialModel.pizza_specials_id, PizzaSpecialModel.pizza_specials_id.in_(sid,)))
    
    if not target:
        return target
    new_attrs = {
        # "store_name": body.store_name, 
        # "store_location": body.store_location,
        # "pizza_specials_id": body.specials,
        "specials_name": body.specials_name,
        "specials_description": body.specials_description,
        "specials_baseprice" : body.specials_baseprice,
        "specials_glutenfree" : body.specials_glutenfree

    }
    for k, v in new_attrs.items():
        setattr(target, k, v)
    db.session.commit()
    db.session.flush()