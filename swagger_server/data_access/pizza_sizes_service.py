# Standard library imports
import json
import os

# Local application imports
from ..database import PizzaSizeModel, db

# SAMPLE_PATH = "data_samples/sample_pizza_sizes.json"

def get_all_pizza_sizes_from_db():
    return PizzaSizeModel.query.all()

def get_pizza_size_by_id(id):
    return PizzaSizeModel.query.get(id)

def create_pizza_size(body):
    data = PizzaSizeModel(body.name, body.measurement, body.size_price)
    db.session.add(data)
    db.session.commit()
    return data

def update_pizza_size_by_id(id, body):
    target = db.session.query(PizzaSizeModel).get(id)
    if not target:
        return target
    new_attrs = {
        "name": body.name, 
        "measurement": body.measurement, 
        "size_price": body.size_price
    }
    for k, v in new_attrs.items():
        setattr(target, k, v)
    db.session.commit()
    db.session.flush()

    return target

def delete_pizza_size_by_id(id):
    target = PizzaSizeModel.query.get(id)
    if not target:
        return target
    db.session.delete(target)
    db.session.commit()
    return target

# def read_from_sample():
#     THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#     # print(os.path.dirname(os.path.abspath(__file__)))
#     TARGET = os.path.join(THIS_FOLDER, SAMPLE_PATH)
#     # print(os.path.join(THIS_FOLDER, "sample_pizza_sizes.json"))
#     with open(TARGET, "r") as data:
#         return json.loads(data.read())

