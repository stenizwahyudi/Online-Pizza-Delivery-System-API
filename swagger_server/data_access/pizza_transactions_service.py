# Standard library imports
import json
import os

# Local application imports
from ..database import OrderModel, PizzaTransactionModel, db

def get_receipts_from_db():
    return PizzaTransactionModel.query.all()

def get_receipt_by_order_id(order_id):
    return PizzaTransactionModel.query.filter(PizzaTransactionModel.pizza_order_id == order_id).all()

def create_receipt(body):
    data = PizzaTransactionModel(body.pizza_receipt_id,
                                 body.pizza_order_id, 
                                 body.name,
                                 body.card_number,
                                 body.card_cvc,
                                 body.card_expiration_year,
                                 body.card_expiration_month,
                                 body.card_billing_address,
                                 body.city,
                                 body.state,
                                 body.zip_code,
                                 body.phone_number,
                                 body.order_time)
    db.session.add(data)
    db.session.commit()
    return data
