# Import flask
from flask import Flask

# Define the WSGI application object
app = Flask(__name__)

# Set config
app.config.from_object('config.DevelopmentConfig')

# Register modules for endpoints
from .endpoints import products_app, cart_app
app.register_blueprint(products_app, url_prefix='/api/v1/products')
app.register_blueprint(cart_app, url_prefix='/api/v1/cart')
