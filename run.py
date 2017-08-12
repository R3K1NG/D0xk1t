#!/usr/bin/python

##### Flask Application Dependencies #####
from config import *

from flask import Flask
from flask import render_template, redirect, url_for, flash, request, session
from flask import jsonify, Response
from flask_googlemaps import GoogleMaps, Map
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, IPAddress, InputRequired
from flask_bootstrap import Bootstrap
from flask_googlemaps import GoogleMaps
from flask_nav import Nav
from flask_nav.elements import Navbar, View

##### Other Dependencies #####

import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict
from uuid import getnode as get_mac
import os, sys, getpass, socket, requests, signal, csv
from datetime import datetime
from time import gmtime, strftime, time
from whois import whois
import pygeoip


# Start App and load configurations
app = Flask(__name__)
app.config.from_object('config')

# Flask-Bootstrap
Bootstrap(app)

# Load up Google Maps
GoogleMaps(app)

# Load up Flask_Nav
nav = Nav()

app.secret_key = SECRET_KEY
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['GOOGLEMAPS_KEY'] = GOOGLEMAPS_API_KEY
app.config['ONLINE_LAST_MINUTES'] = ONLINE_LAST_MINUTES
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doxkit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

class DoxForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    age = IntegerField('Age')
    dob = DateField('Date of Birth')
    address = TextAreaField('First Line Address')
    address1 = TextAreaField('Second Line Address')
    citystate = StringField('City and State')
    zipcode = StringField('ZIP Code')
    ipaddress = StringField('IP Address', validators=[IPAddress()])

class GeoIPForm(FlaskForm):
    ip = StringField('IP Address', validators=[IPAddress()])

class DNSForm(FlaskForm):
    url = StringField('Domain Name', [InputRequired()], render_kw={"placeholder": "example.com"})


##### Initialize Database #####
db = SQLAlchemy(app)


class Doxkit(db.Model):
    __tablename__ = "dox"
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    age = Column(Integer, unique=False)
    dob = Column(String(10), unique=False)
    address = Column(String(50), unique=True)
    address1 = Column(String(50), unique=True)
    citystate = Column(String(50), unique=False)
    zipcode = Column(Integer, unique=False)
    ipaddress = Column(String(25), unique=True)

    def __init__(self, name, age, dob, address, 
      address1, citystate, zipcode, ipaddress):
        self.name = name
        self.age = age
        self.dob = dob
        self.address = address
        self.address1 = address1
        self.citystate = citystate
        self.zipcode = zipcode
        self.ipaddress = ipaddress
    
    def __repr__(self):
        return '<Name {0}>'.format(self.name)

##### Signal Handler to Kill safely as well as actual application #####
def signal_handler(signal, frame):
    print "Killing D0xk1t. Thanks for playing!"
    sys.exit(0)
        
# Start signal handler
signal.signal(signal.SIGINT, signal_handler)


##### Global variables to display eye candy #####
user  = socket.gethostname()
localhost = socket.gethostbyname(user)
lan_ip = os.popen("ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'").read()

@app.before_first_request
def setup():
    db.create_all()


# Redirect to /index or /login depending on login session
@app.route('/')
def hello():
    return redirect(url_for('index'))

# Dashboard
@app.route('/index')
def index():
    return render_template('index.html',
                            user=user,
                            title="Admin Dashboard",
                            small="Welcome to D0xk1t!",
                            localhost=localhost, # Localhost address
                            lan_ip=lan_ip,  # LAN Address
                            ) 
# Dox module
@app.route('/dox', methods=['GET', 'POST'])
def dox():
    description = """  The D0x module is a comprehensive info-gathering database that enables the pentester
    to write "D0x", or a file that holds a collection of data of a certain target, or targets.
    Using this data, the tester will be able to effectively understand their target, which is a
    critical point in the attacker's kill chain. Usually deemed malicious and black-hat in nature,
    the D0x module, however, aims to help security researchers gain momentum when conducting in-the-field
    pentesting. <br /> The D0x module does come with several features, improved upon based off of the prior
    revision. Not only does it provide an user interface for at-ease use, but also capabilities to store
    already-collected information, as well as import non-D0xk1t written D0x reports."""
        
    form = DoxForm()
    rows = Doxkit.query.all()
    if request.method == "POST":
        d = Doxkit(request.form['name'], request.form["age"], request.form["dob"],
            request.form["address"], request.form["address1"], request.form["citystate"],
            request.form["zipcode"], request.form["ipaddress"])
        db.session.add(d)
        db.session.commit()        
        flash("D0x created successfully!", "success")
    return render_template('dox.html',
                            title="D0x Module",
                            small="Writing comprehensive reports for the purpose of information gathering",
                            user=user,
                            description=description,
                            form=form, rows=rows)

# Delete-dox GET request
@app.route('/delete-dox/<delete_id>', methods=['GET'])
def deletedox(delete_id):
    Doxkit.query.filter_by(id=delete_id).delete()
    db.session.commit()
    flash("Deleted query!", "success")
    return redirect(url_for('dox')) 

# Export-dox command
@app.route('/export-dox/<export_id>', methods=['GET'])
def exportdox(export_id):
    time = strftime("%Y-%m-%d-%H:%M:%S", gmtime())    
    _csv = open('{}.csv'.format(time), 'wb')
    outcsv = csv.writer(_csv)
    records = db.session.query(Doxkit).all()
    [outcsv.writerow([getattr(curr, column.name) for column in Doxkit.__mapper__.columns]) for curr in records]
    _csv.close()
    flash("Exported Dox! Stored in your D0xk1t path.", "success")
    return redirect(url_for('dox'))                     

# GeoIP Module
@app.route('/geoip', methods=['GET', 'POST'])
def geoip():
    form = GeoIPForm()
    description = """
    When working with metadata, IP addresses often pop up as a point-of-interest.
    Using Maxmind and Google Map's APIs, the GeoIP module aims to collect geolocation
    information on public IP addresses, in order to gather data on physical location during
    the reconaissance stage of the killchain. In order to make this module work, please provide a <a href="https://developers.google.com/maps/documentation/javascript/get-api-key">Google Maps API key</a>.
    """
    if request.method == "POST":
        geoip = pygeoip.GeoIP("src/GeoLiteCity.dat")
        try:
            ip_data = geoip.record_by_addr(request.form['ip'])
            return render_template('geoip.html', title="GeoIP Module", user=user, description=description, form=form, latitude=ip_data["latitude"], longitude=ip_data["longitude"], ip_data=ip_data)
        except (TypeError, ValueError, socket.error):
            flash("Invalid IP Address provided!", "danger")
            return redirect(url_for('geoip')) 
    else:
        return render_template('geoip.html', title="GeoIP Module", small="Using locational data to conduct info-gathering",
                                user=user, description=description, form=form,
                                latitude="0", longitude="0")
# GeoIP API endpoint    
@app.route('/api/geoip/<ip_address>')
def ipinfo(ip_address):
    geoip = pygeoip.GeoIP("app/GeoLiteCity.dat")
    ip_data = geoip.record_by_addr(ip_address)
    return jsonify(ip_data)
    
# DNS Enumeration
@app.route('/dns', methods=['GET', 'POST'])
def dns():
    description = """
    Targets, whether it be a company or a person, may utilize domains in order to
    display web content. Domains, especially those that are not properly configured,
    give penetration testers great opportunity to gather sensitive information in the
    form of metadata, whether it be an address from a WHOIS lookup, or nameservers."""
    form = DNSForm()
    if request.method == "POST":
        whois_data = whois(request.form["url"])
        return render_template('dns.html', title="DNS Enumeration Module", 
                            user=user, description=description, form=form, whois=str(whois_data))
    else:
        return render_template('dns.html', title="DNS Enumeration Module", 
                            user=user,description=description, form=form, whois=None)

# Nmap
@app.route('/nmap')
def nmap():
    description = """
    Nmap is a great tool for every penetration tester, and should be available for
    every pentest. However, Nmap does provide tons of features that may seem very
    complex to implement when using the command-line version. Therefore, the webNmap
    module provides a great interface to the tool, enabling the attacker to efficiently
    scan a network or host during info-gathering."""
    return render_template('nmap.html', title="webNmap Module", description=description,
        small="A great user interface for quick Nmap scanning", user=user)
    
    
if __name__ == '__main__':
    app.run()
    
    

