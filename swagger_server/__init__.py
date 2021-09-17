# Standard library imports
import os

# Third party imports
import connexion
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# Local application imports
from swagger_server import encoder

# some constants
# local postgresql database password and table name
DB_PASSWORD = '123456'
DB_NAME = 'turingpizza'
# get the templates folder dir name
TEMPLATES_FOLDER_DIRNAME = os.path.join(os.path.dirname(__file__).rstrip("swagger_server/"), "templates")
# deployment mode
MODE = 'prod'

# create the app instance
app = connexion.FlaskApp(__name__, specification_dir='./swagger/')
app.app.json_encoder = encoder.JSONEncoder
# read the swagger.yaml file to configure the endpoints
app.add_api('swagger.yaml', arguments={'title': 'Turing Pizza API'}, pythonic_params=True)

if MODE == 'dev':
    app.app.debug = True
    app.debug = True
    # setting string value for connexion app, use app.app.['str_key'] = 'str_val'
    app.app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:{}@localhost/{}".format(DB_PASSWORD, DB_NAME)
else:
    app.app.debug = False
    app.debug = False
    app.app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", None)
app.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# get access to and setup the templates folder dirname
app.app.template_folder = TEMPLATES_FOLDER_DIRNAME

# # create URL route for '/'
@app.route('/')
def home():
    return render_template("home.html")

