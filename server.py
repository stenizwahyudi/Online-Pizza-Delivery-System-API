from flask import Flask, render_template, request

import connexion
from swagger_server import encoder

# some constants
# choose either dev or prod, and port
ENV = "dev"
PORT = 8080
# set database name and database password
DB_NAME = 'turingpizza'
DB_PASSWORD = '123456'

# create the app instance
app = connexion.FlaskApp(__name__, specification_dir='./swagger_server/swagger/')
app.app.json_encoder = encoder.JSONEncoder
# read the swagger.yaml file to configure the endpoints
app.add_api('swagger.yaml', arguments={'title': 'Turing Pizza API'}, pythonic_params=True)

if ENV == 'dev':
    app.app.debug = True
    # setting string value for connexion app, use app.app.['str_key'] = 'str_val'
    app.app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:{}@localhost/{}".format(DB_PASSWORD, DB_NAME)
else:
    app.app.debug = False
    app.app.config["SQLALCHEMY_DATABASE_URI"] = ""
app.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# # create URL route for '/'
@app.route('/')
def home():
    return render_template('home.html')

# if running in stand alone mode, then run the app, also in debug mode
if __name__ == '__main__':
    app.run(port=PORT, debug=ENV=="dev")

