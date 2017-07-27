#!/usr/bin/python

##### Flask Application Dependencies #####
from app import app
from config import *
from app.forms import DoxForm, LoginForm, GeoIPForm

from flask import render_template, redirect, url_for, flash, request, session
from flask import jsonify, Response
from flask_googlemaps import GoogleMaps, Map
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

from redis import Redis

##### Other Dependencies #####

import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict
from uuid import getnode as get_mac
import os, sys, getpass, socket, requests, signal, csv
from datetime import datetime
from time import gmtime, strftime, time
import pygeoip

app.secret_key = SECRET_KEY
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['GOOGLEMAPS_KEY'] = GOOGLEMAPS_API_KEY
app.config['ONLINE_LAST_MINUTES'] = ONLINE_LAST_MINUTES
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doxkit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

##### Start Redis Server #####

os.system("sudo /etc/init.d/redis-server start")

##### Initialize Database #####
db = SQLAlchemy(app)

def create_db():
    os.system("touch app/doxkit.db")
    db.create_all()

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

##### Signal Handler to Kill safely as well as actual application #####
def signal_handler(signal, frame):

    print "Killing D0xk1t. Thanks for playing!"
    sys.exit(0)
        
# Start signal handler
signal.signal(signal.SIGINT, signal_handler)


##### Global variables to display eye candy #####
user  = getpass.getuser()
localhost = socket.gethostbyname(socket.gethostname())
lan_ip = os.popen("ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'").read()

config_file = open("app/configure.txt").read()


##### Dependency Checker based on requirements.txt changes #####
dependency_check = "INSTALLED" # flag = 0
with open('requirements.txt', 'rb') as f:
    for line in f:
        dependencies = line.rstrip()
        
# If not installed, change dependency_check flag
try:
    pkg_resources.require(dependencies)
except (DistributionNotFound, VersionConflict):
    dependency_check = "NOT_INSTALLED" # flag = 1 

# Start first-init, if necessary
if config_file == "NEW_CONFIGURATION":
    print("Initializing First Boot!")
    with open("app/configure.txt", "wb") as overwrite:
        overwrite.write("OLD_CONFIGURATION")
    create_db()

##### Getting active users #####
redis = Redis()
def mark_online(user_id):
    now = int(time())
    expires = now + (app.config['ONLINE_LAST_MINUTES'] * 60) + 10
    all_users_key = 'online-users/%d' % (now // 60)
    user_key = 'user-activity/%s' % user_id
    p = redis.pipeline()
    p.sadd(all_users_key, user_id)
    p.set(user_key, now)
    p.expireat(all_users_key, expires)
    p.expireat(user_key, expires)
    p.execute()
    
def get_user_last_activity(user_id):
    last_active = redis.get('user-activity/%s' % user_id)
    if last_active is None:
        return None
    return datetime.utcfromtimestamp(int(last_active))

def get_online_users():
    current = int(time()) // 60
    minutes = xrange(app.config['ONLINE_LAST_MINUTES'])
    return redis.sunion(['online-users/%d' % (current - x)
                         for x in minutes])

@app.before_request
def mark_current_user_online():
    mark_online(user)

active_users = '%s' % ', '.join(get_online_users())
###############################################################################

# In the case page is not found (404), render 404.html    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Redirect to /index or /login depending on login session
@app.route('/')
def hello():
    if session.get('logged_in'):
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


# Login/logout routes    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST':
        if (request.form['username'] == USER_LOGIN) and (request.form['password'] == USER_PASSWORD):            
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash("Login Failed! Could not authenticate.", "danger") 
            return redirect(url_for('login'))
    return render_template('login.html', form=form, title="Login - D0xk1t")

@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash("Logged out successfully!", "success") 
    return redirect(url_for('login'))

# FAQ
@app.route('/faq')
def faq():
    return render_template('faq.html', title="Frequently Asked Question - D0xk1t")

# API Docs
@app.route('/develop')
def develop():
    return render_template('develop.html', title="API Docs - D0xk1t")

# Dashboard
@app.route('/index')
def index():
    if session.get('logged_in'):
        return render_template('index.html',
                                user=user, # Username
                                localhost=localhost, # Localhost address
                                lan_ip=lan_ip,  # LAN Address
                                dependency_check=dependency_check,
                                active_users=active_users
                                ) 
    else:
        flash("Hey! Login first!", "warning")
        return redirect(url_for('login')) 

# Dox module
@app.route('/dox', methods=['GET', 'POST'])
def dox():
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
                            user=user,
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
    if request.method == "POST":
        geoip = pygeoip.GeoIP("app/GeoLiteCity.dat")
        try:
            ip_data = geoip.record_by_addr(request.form['ip'])
            return render_template('geoip.html', title="GeoIP Module", user=user, form=form, latitude=ip_data["latitude"], longitude=ip_data["longitude"], ip_data=ip_data)
        except (TypeError, ValueError, socket.error):
            flash("Invalid IP Address provided!", "danger")
            return redirect(url_for('geoip')) 
    else:
        return render_template('geoip.html', title="GeoIP Module", user=user, form=form,
                                latitude="0", longitude="0")
# GeoIP API endpoint    
@app.route('/api/geoip/<ip_address>')
def ipinfo(ip_address):
    geoip = pygeoip.GeoIP("app/GeoLiteCity.dat")
    ip_data = geoip.record_by_addr(ip_address)
    return jsonify(ip_data)
    
    
if __name__ == '__main__':
    app.run()
    
    

