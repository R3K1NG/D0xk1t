#!venv/bin/python

##### Flask Application Dependencies #####
from app import app
from config import *
from app.forms import DoxForm, LoginForm, GeoIPForm, MailForm
from flask import render_template, redirect, url_for, flash, request, session
from flask import jsonify, Response
from flask_googlemaps import GoogleMaps, Map
from flask_mail import Mail
from redis import Redis

##### Other Dependencies #####

import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict
from uuid import getnode as get_mac
import os, sys, getpass, socket, requests, threading, signal, atexit, shutil, time
from datetime import datetime
import pygeoip,  psutil

app.secret_key = SECRET_KEY
app.config['GOOGLEMAPS_KEY'] = GOOGLEMAPS_API_KEY
app.config['ONLINE_LAST_MINUTES'] = ONLINE_LAST_MINUTES


##### Signal Handler to Kill Threading safely as well as actual application #####
def signal_handler(signal, frame):
    #atexit.register(time_increment)
    #t.cancel()
    #t1.cancel()
    print "Killing D0xk1t. Thanks for playing!"
    sys.exit(0)
        
# Start signal handler
signal.signal(signal.SIGINT, signal_handler)


##### Global variables for display eye candy #####
user  = getpass.getuser()
localhost = socket.gethostbyname(socket.gethostname())
lan_ip = os.popen("ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'").read()


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

'''
##### Threading Timer for background minute incrementing #####
mins = 0 
def time_increment(mins):
    mins = mins + 1
    print mins

def async():
    t = threading.Timer(2.0, time_increment, [mins]).start()
    t1 = threading.Timer(2.0, async).start()

async()
'''

##### Getting active users #####
redis = Redis()
def mark_online(user_id):
    now = int(time.time())
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
    current = int(time.time()) // 60
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
    if request.method == "POST":
        doxfile = "%sDox" % request.form['name']
        with open(doxfile, 'a') as d:
            d.write("Name: " + str(request.form['name']) + "\n")
            d.write("Age: " + str(request.form["age"]) + "\n")
            d.write("Date of Birth: " + str(request.form["dob"]) + "\n")
            d.write("First Line Address: " + str(request.form["address"]) + "\n")
            d.write("Second Line Address: " + str(request.form["address1"]) + "\n")
            d.write("City & State: " + str(request.form["citystate"]) + "\n")
            d.write("Postal Code: " + str(request.form["zipcode"]) + "\n")
            d.write("IP Address: " + str(request.form["ipaddress"]) + "\n")
        flash("D0x created successfully!", "success")
    return render_template('dox.html',
                            title="D0x Module",
                            user=user,
                            form=form)
                            
@app.route('/dox/<flag>',)
def dox_flag(flag):
    if flag == "success":
        return render_template('success.html')
    else:
        flash("Failed")


# GeoIP Module
@app.route('/geoip', methods=['GET', 'POST'])
def geoip():
    form = GeoIPForm()
    if request.method == "POST":
        geoip = pygeoip.GeoIP("app/GeoLiteCity.dat")
        ip_data = geoip.record_by_addr(request.form['ip'])
        return render_template('geoip.html', title="GeoIP Module", user=user, form=form,                             latitude=ip_data["latitude"], longitude=ip_data["longitude"], ip_data=ip_data)
    else:
        return render_template('geoip.html', title="GeoIP Module", user=user, form=form,
                                latitude="0", longitude="0")
        
@app.route('/api/geoip/<ip_address>')
def ipinfo(ip_address):
    geoip = pygeoip.GeoIP("app/GeoLiteCity.dat")
    ip_data = geoip.record_by_addr(ip_address)
    return jsonify(ip_data)

@app.route('/massmail')
def massmail():
    form = MailForm()
    if request.method == "POST":
        return "good"
    else:
        return render_template("massmail.html", title="Mass Mailer Module", user=user, form=form)
        
if __name__ == '__main__':
    try:
        os.system("sudo /etc/init.d/redis-server start")
    except:
        sys.exit("Redis couldn't be started. Is it installed?")
    app.run()
    
    

