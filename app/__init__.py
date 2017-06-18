from flask import Flask
from flask_bootstrap import Bootstrap
from flask_googlemaps import GoogleMaps
from flask_mail import Mail

# Start App and load configurations
app = Flask(__name__)
app.config.from_object('config')

# Flask-Bootstrap
Bootstrap(app)

# Load up Google Maps
GoogleMaps(app)

# Load Flask Mail
mail = Mail(app)

# Other Flask dependencies
from app import forms
