# standard libs imports
import time

# Third party imports
from flask_sqlalchemy import SQLAlchemy

# Local application imports
from swagger_server import app

# make the db object
db = SQLAlchemy(app.app)

class PizzaSizeModel(db.Model):
    __tablename__ = 'pizza_sizes'
    pizza_sizes_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    measurement = db.Column(db.Float)
    size_price = db.Column(db.Float)

    def __init__(self, name, measurement, size_price):
      self.name = name
      self.measurement = measurement
      self.size_price = size_price

class PizzaToppingModel(db.Model):
    __tablename__ = 'pizza_toppings'
    pizza_toppings_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    topping_price = db.Column(db.Float)
    gluten_free = db.Column(db.Boolean)

    def __init__(self, name, topping_price, gluten_free):
        self.name = name
        self.topping_price = topping_price
        self.gluten_free = gluten_free

class PizzaStoreModel(db.Model):
    __tablename__ = 'pizza_store'
    pizza_stores_id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(100))
    store_location = db.Column(db.String(100))
    # pizza_specials_id = db.Column(db.ARRAY(db.Integer, db.ForeignKey("pizza_special.pizza_specials_id")))
    pizza_specials_id = db.Column(db.ARRAY(db.Integer))

    def __init__(self,store_name, store_location, pizza_specials_id):
        self.store_name = store_name
        self.store_location = store_location
        self.pizza_specials_id = pizza_specials_id

class PizzaSpecialModel(db.Model):
    __tablename__ = 'pizza_special'
    pizza_specials_id = db.Column(db.Integer, primary_key=True)
    specials_name = db.Column(db.String(100))
    specials_description = db.Column(db.String(100))
    specials_baseprice = db.Column(db.Float) 
    specials_glutenfree = db.Column(db.Boolean)
    

    def __init__(self,specials_name, specials_description, specials_baseprice, specials_glutenfree):
        self.specials_name = specials_name
        self.specials_description = specials_description
        self.specials_baseprice = specials_baseprice
        self.specials_glutenfree = specials_glutenfree


class PizzaModel(db.Model):
    __tablename__ = 'pizza'
    pizza_id = db.Column(db.Integer, primary_key=True)
    pizza_count= db.Column(db.Integer)
    pizza_totalprice = db.Column(db.Float)
    pizza_specials_id = db.Column(db.Integer, db.ForeignKey("pizza_special.pizza_specials_id"))
    # pizza_toppings_id = db.Column(db.Integer, db.ForeignKey("pizza_toppings.pizza_toppings_id"))
    pizza_toppings_id = db.Column(db.ARRAY(db.Integer))
    pizza_sizes_id = db.Column(db.Integer, db.ForeignKey("pizza_sizes.pizza_sizes_id"))
    
    

    def __init__(self,pizza_count, pizza_totalprice, pizza_specials_id, pizza_toppings_id, pizza_sizes_id):
        self.pizza_count = pizza_count
        self.pizza_totalprice = pizza_totalprice
        self.pizza_specials_id = pizza_specials_id
        self.pizza_toppings_id = pizza_toppings_id
        self.pizza_sizes_id = pizza_sizes_id

class OrderModel(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, primary_key=True)
    order_totalprice= db.Column(db.Float)
    # pizza_id = db.Column(db.Integer, db.ForeignKey("pizza.pizza_id"))
    pizza_id = db.Column(db.ARRAY(db.Integer))
    pizza_stores_id = db.Column(db.Integer, db.ForeignKey("pizza_store.pizza_stores_id"))

    def __init__(self, order_totalprice, pizza_id, pizza_stores_id):
        self.order_totalprice = order_totalprice
        self.pizza_id = pizza_id
        self.pizza_stores_id = pizza_stores_id

class PizzaTransactionModel(db.Model):
    __tablename__ = 'pizza_receipts'
    pizza_receipt_id = db.Column(db.Integer, primary_key = True)
    pizza_order_id = db.Column(db.Integer, db.ForeignKey("order.order_id"))
    name = db.Column(db.String(100))
    card_number = db.Column(db.String(16))
    card_cvc = db.Column(db.String(3))
    card_expiration_year = db.Column(db.String(4))
    card_expiration_month = db.Column(db.String(2))
    card_billing_address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zip_code = db.Column(db.String(10))
    phone_number = db.Column(db.String(100))
    order_time = db.Column(db.String(100))

    def __init__(self,  pizza_receipt_id,
                                  pizza_order_id, 
                                  name,
                                  card_number,
                                  card_cvc,
                                  card_expiration_year,
                                  card_expiration_month,
                                  card_billing_address,
                                  city,
                                  state,
                                  zipcode,
                                  phone_number,
                                  order_time):
        self.pizza_receipt_id = int(round(time.time()%10000007 + 33)),
        self.pizza_order_id = pizza_order_id,
        self.name = name,
        self.card_number = card_number,
        self.card_cvc = card_cvc,
        self.card_expiration_year = card_expiration_year,
        self.card_expiration_month = card_expiration_month,
        self.card_billing_address = card_billing_address,
        self.city = city,
        self.state = state,
        self.zipcode = zipcode,
        self.phone_number = phone_number,
        self.order_time = order_time

