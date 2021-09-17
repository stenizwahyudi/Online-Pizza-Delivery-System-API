import connexion
import six
import datetime

from swagger_server.models.transactions import Transactions  # noqa: E501
from swagger_server import util

from ..data_access import pizza_transactions_service, pizza_orders_service


def get_receipt_by_order_id(pizza_order_id):  # noqa: E501
    """Get receipt by Order ID.

    Get receipt by Order ID.  # noqa: E501

    :param pizza_order_id: The Id of the order to be queried. 
    :type pizza_order_id: int

    :rtype: Transactions
    """
    found_order = pizza_orders_service.get_order_by_id(pizza_order_id)
    if not found_order:
        return {'error': 'No order found for the given ID.'}, 404
    else:
        body = pizza_transactions_service.get_receipt_by_order_id(pizza_order_id)
        if not body:
            return {"error": "No receipt found for this order ID. "}, 404
        body = body[0]
        new_card_number = '***'+ body.card_number[-4:]
        new_cvc = '*'*len(body.card_cvc)
        found = Transactions(body.pizza_receipt_id,
                                 body.pizza_order_id, 
                                 body.name,
                                 new_card_number,
                                 new_cvc,
                                 body.card_expiration_year,
                                 body.card_expiration_month,
                                 body.card_billing_address,
                                 body.city,
                                 body.state,
                                 body.zip_code,
                                 body.phone_number,
                                 body.order_time)
        return found, 200


def get_receipts():  # noqa: E501
    """Get all available receipts.

    Access to all Receipts. Return all as an object array.  # noqa: E501


    :rtype: List[Transactions]
    """
    data = pizza_transactions_service.get_receipts_from_db()
    transactions = list()
    for body in data:
        new = Transactions(body.pizza_receipt_id,
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
        transactions.append(new)
    return transactions, 200

def create_receipt(body, pizza_order_id):
    """Create a new receipt for the given order ID.

    Create a new receipt for the given order ID.  # noqa: E501
    
    :param body: Transaction object that needs to be stored in database
    :type body: dict | bytes
    :param pizza_order_id: The Id of the pizza order to be queried. 
    :type pizza_order_id: int

    :rtype: Transactions
    """

    if connexion.request.is_json:
        body = Transactions.from_dict(connexion.request.get_json())  # noqa: E501

    found_order = pizza_orders_service.get_order_by_id(pizza_order_id)
    if not found_order:
        return {'error': 'No order found for the given ID.'}, 404

    receipts_for_given_order_id = pizza_transactions_service.get_receipt_by_order_id(pizza_order_id)
    if len(receipts_for_given_order_id) > 0:
        return {'error': "The receipt for given order id already exists. "}, 400
        
    today = datetime.datetime.now()
    if len(body.card_number) != 16 or not body.card_number.isdigit():
        return {'error': "Please input a valid credit card number. "}, 404
    if len(body.card_cvc) != 3 or not body.card_cvc.isdigit():
        return {'error': "Please input a valid credit card cvc number. "}, 404
    if int(body.card_expiration_month) > 12 or int(body.card_expiration_month) < 1:
        return {'error': "Please input a valid credit card expiration month. "}, 404
    if int(body.card_expiration_year) < today.year:
        return {'error': "Please input a valid credit card expiration year. "}, 404    
    if int(body.card_expiration_year) == today.year and int(body.card_expiration_month) < today.month:
        return {'error': "Please input a valid credit card expiration year. "}, 404
    if len(body.phone_number) != 10 or not body.phone_number.isdigit():
        return {'error': "Please input a valid phone number. "}, 404

    body.pizza_order_id = pizza_order_id
    data = pizza_transactions_service.create_receipt(body)
    new = Transactions(data.pizza_receipt_id,
                                 pizza_order_id, 
                                 data.name,
                                 data.card_number,
                                 data.card_cvc,
                                 data.card_expiration_year,
                                 data.card_expiration_month,
                                 data.card_billing_address,
                                 data.city,
                                 data.state,
                                 data.zip_code,
                                 data.phone_number,
                                 data.order_time)
    return new, 200