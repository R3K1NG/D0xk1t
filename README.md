![logo](/extras/logo.png)

Active reconaissance and information gathering built in a portable web application_

---

## NOTE

Looking for the older version of D0xk1t? Check inside the `script` folder, where all of the original code is retained in its glorious crappy form.

This revision is not at all production-quality! I am only releasing it publicly for code review. Still, this does not mean that I won't be working on this!


![logo](/extras/screenshot.png)


## 1.0 Introduction

1. What is this? 

D0xk1t is an __open-source__, __self-hosted__ and __easy to use__ active 
reconaissance web application for penetration testers. Based off of the prior
command-line script, D0xk1t is now fully capable of conducting reconaissance
and penetration testing for security researchers who need a framework without the 
head-scratching.

2. Is this a website / webapp ?

Yes and no. In essence, it is not a typical website. D0xk1t is self-hosted. There is no server stack, cloud-based service, SaaS, etc. that is holding it up. You can have the option of deploying D0xk1t on a local network, or deploying
your own instance on any infrastructure / technology as you wish. Although not recommended, for security purposes, change the default authentication if you wish to expose to the Internet.

3. Is this free ?

Yes. D0xk1t will forever be open-source. If you wish to contribute, you can make a fork, add any changes, and send a pull request on Github.

4. How else can I develop on this?

I am currently working on API endpoints for D0xk1t. 

---

## 2.0 Features

* Easy-to-build, risk-free installation
* Simple Bootstrap Admin Dashboard
* Deployable to the Internet
* Serverless (at the moment)
* Expansive to any OS

---

## 3.0 Installation 

Since D0xk1t is self-hosted, it does not work immediately out-of-box. It is recommended that you use a `virtualenv` container due to the sheer number of dependencies that can run into conflict with your Python configuration.

### 3.1 Building

__Core Dependencies:__

* Python 2.7.x
* python-pip 
* virtualenv 
* redis-server
* Git

Lucky for you, there are two ways to build D0xk1t. The __quick 'n easy way__, and the __manual way__.

__Quick 'n Easy Way:__

     $ curl https://raw.githubusercontent.com/ex0dus-0x/D0xk1t/master/extras/install | sudo /bin/bash 

__Manual Way:__

    $ git clone https://github.com/ex0dus-0x/D0xk1t && cd D0xk1t
    $ source venv/bin/activate
    $ pip install -r requirements.txt

### 3.2 Configuration

Open `config.py`. Here, you will see all the environmental variables that the application utilizes. Three important fields you __MUST__ be aware of if you plan to deploy to the web.

    GOOGLEMAPS_API_KEY = "YOUR_API_KEY_HERE"

    SECRET_KEY = 'SECRET_KEY_HERE'

    USER_LOGIN = "hackerman"
    USER_PASSWORD = "password"
    
`GOOGLEMAPS_API_KEY` denotes the Google Maps API Key. This is essential for the GeoIP module. You can obtain it [here](https://developers.google.com/maps/) and change the variable accordingly.

`SECRET_KEY` is the private key utilized by WTForm's CSRF protection feature. If deployed, change it to your liking.

`USER_LOGIN` and `USER_PASSWORD` are the variables for authentication. Since D0xk1t is currently serverless, these variables contain the user and password pair when you login to D0xk1t. Of course, if you plan to deploy to the web, __CHANGE THESE!__ otherwise anyone will be able to login with these default credentials.


### 3.3 Deployment

Once installed, run with `python run.py`. The application is accessible at `127.0.0.1:5000`. Login with credentials, and you will be present with the admin panel.

Of course, this is self-hosting on localhost. Although work-in-progress, D0xk1t will soon support hosting on a variety of SaaS and server stacks of your choice.

* [Heroku](https://www.heroku.com/) - __TODO__: build a `Procfile`, as well as bash scripts for automatic deployment
* [ngrok](https://ngrok.com/) - __TODO__: build a script for deployment to ngrok

---

## 4.0 Modules

#### D0x Module

The D0x module is a comprehensive info-gathering database that enables the pentester
to write "D0x", or a file that holds a collection of data of a certain target, or targets.
Using this data, the tester will be able to effectively understand their target, which is a
critical point in the attacker's kill chain. D0xing is usually deemed malicious and black-hat in nature. However, with the D0x module, we aim to help security researchers gain momentum when conducting in-the-field pentesting. The D0x module does come with several features, improved upon based off of the prior revision. 

#### GeoIP Module 

When working with metadata, IP addresses often pop up as a point-of-interest.
Using Maxmind and Google Map's APIs, the GeoIP module aims to collect geolocation
information on public IP addresses, in order to gather data on physical location during
the reconaissance stage of the killchain.

---

### 5.0 TODO

* More modules!
  * include mass mailer, wordlist generation, D0x Module DB support (w/ SQLalchemy, Redis and/or SQLite)
  * API endpoints
* Build scripts for web deployment
* Fix `TypeError` and `ValueError` for GeoIP when non-recognized IP address is inputted.
* Make website! Surge or Github Pages
