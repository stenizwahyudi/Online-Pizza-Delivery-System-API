# Standard library imports
import json
import os

# Local application imports
from ..database import OrderModel, db
from .pizzas_service import get_pizza_by_id

def get_all_orders_from_db():
    return OrderModel.query.all()

def get_order_by_id(id):
    return OrderModel.query.get(id)

def create_order(body):
    # when create a new order, by default the 
    # total price is 0, since pizzas are not 
    # posted yet
    # so pizza id list is also empty
    total_price = 0
    pizza_id_list = list()
    data = OrderModel( 
        total_price, 
        pizza_id_list,
        body.pizza_store_id)
    db.session.add(data)
    db.session.commit()
    return data

def update_order_by_id(id, body):
    target = db.session.query(OrderModel).get(id)
    if not target:
        return target
    # get the new total price
    new_total_price = get_order_total_price(body)
    new_attrs = {
        "order_totalprice": new_total_price, 
        "pizza_id": body.pizzas_id, 
        "pizza_stores_id": body.pizza_store_id
    }
    for k, v in new_attrs.items():
        setattr(target, k, v)
    db.session.commit()
    db.session.flush()

    return target

def delete_order_by_id(id):
    target = OrderModel.query.get(id)
    if not target:
        return target
    db.session.delete(target)
    db.session.commit()
    return target

def get_order_total_price(order):
    total_price = 0
    # for a new order, pizza id list is empty, so return 0
    if not order.pizzas_id:
        return total_price
    # assume the pizza id in the order is valid
    for pizza_id in order.pizzas_id:
        total_price += get_pizza_by_id(pizza_id).pizza_totalprice
    return total_price

