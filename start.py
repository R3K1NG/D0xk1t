#!/usr/bin/python
import sys, time, platform		# "Preprocessor directives" because I'm used to C++
import pip
from subprocess import call
from getpass import getpass

W = '\033[0m'  # white (normal)
R = '\033[31m'  # red
G = '\033[32m'  # green					# Variables for text colors. Saves me the trouble thank you!
O = '\033[33m'  # orange
B = '\033[34m'  # blue
P = '\033[35m'  # purple
C = '\033[36m'  # cyan
GR = '\033[37m'  # gray

# New dependencies
try:
	import nmap
	import GeoIP
	import urllib
	import urllib2
	import re
	import smtplib
	from geoip import geolite2
	from lxml import html
	from email.mime.text import MIMEText
except ImportError:
	print R + "You are missing dependencies. They will be installed with pip" + W
	print "Loading..."
	time.sleep(3)
	pip.main(['install', 'python-nmap', 'python-geoip', 'python-geoip-geolite2'])

#Function for writing a D0x.
def dox():

	print G + "Let's get started, shall we?" + W
	print B + "If you don't know info, just leave a blank" + W
	#First Name
	name = raw_input("[>] First, give me a " + P + " FULL NAME: " + W)
	text_file = open("Dox of %s" % name, 'a')
	text_file.write("Name: %s" % name)
	#Age
	age = raw_input("[>] What is the " + P + "AGE " + W + "of this person? ")
	text_file = open("Dox of %s" % name, 'a')
	text_file.write("\nAge: %s" % age)
	#Date of Birth
	dob = raw_input("[>] What is the " + P + "DATE OF BIRTH?" + W + "(month/day/year): ")
	text_file = open("Dox of %s" % name, 'a')
	text_file.write("\nDate of Birth: %s" % dob)
	#First Line of Address
	faddress = raw_input("[>] Next, give me the first line of the " + P + "ADDRESS " + W + "(e.g 123-12 4th St.): ")
	text_file = open("Dox of %s" % name, 'a')
	text_file.write("\nFirst Line of Address: %s" % faddress)
	#Second Line of Address
	saddress = raw_input("[>] OK, if there is, give me a second line of the " + P + "ADDRESS " + W + "(e.g Apartment 4): ")
	text_file = open("Dox of %s" % name, 'a')
	text_file.write("\nSecond Line of Address: %s" % saddress)
	#City and State
	cands = raw_input("[>] OK, give me the " + P  + "CITY and STATE " + W + "in this format: City, State Initials: ")
	text_file = open("Dox of %s" % name, 'a')
	text_file.write("\nCity and State: %s" % cands)
	#ZIP Code
	zipc = raw_input("[>] What's the " + P + "ZIP Code" + W + "? ")
	text_file = open("Dox of %s" % name, 'a')
	text_file.write("\nZIP Code: %s" % zipc)
	#IPv4 Address
	ipadd = raw_input("[>] Now, gimme the " + P + "IP address: " + W)
	text_file = open("Dox of %s" % name, 'a')
	text_file.write("\nIP Address: %s" % ipadd)
	#Emails
	print G + "This next part requires you to enter the emails of the victim. Once you are finished, enter " + R + "quit" + W
	print B + "If you know the password, place in this format: " + GR + "user@email:password" + W
	print B + "^ This applies for the Facebook, Twitter and Other Aliases! Please use account:password format!" + W

	while True:
		email = raw_input("[>] Give me an email! ")
		if email == "quit":
			break
		else:
			text_file = open("Dox of %s" % name, 'a')
			text_file.write("\nEmail: %s" % email)
	#Facebook
	facebook = raw_input("[>] What about " + P + "Facebook? " + W + "Please give a link! ")
	text_file = open("Dox of %s" % name, 'a')
	text_file.write("\nFacebook: %s" % facebook)

	#Twitter
	twitter = raw_input("[>] Got " + P + "Twitter? " + W + "Please give a link! ")
	text_file = open("Dox of %s" % name, 'a')
	text_file.write("\nTwitter: %s" % twitter)

	#Other aliases
	print G + "OK if you got other aliases, such as LinkedIN, Instagram, Snapchat, Spotify, etc. you can also include!" + W
	print B + "When you enter something, please format like so: Alias: user/link:optionalpassword" + W
	print B + "Again, if you know the password, include that too! Enter" + R + "quit" + B + "when you are done!" + W

	while True:
		alias = raw_input("[>]")
		if alias == "quit":
			break
		else:
			text_file = open("Dox of %s" % name, 'a')
			text_file.write("\n%s" % alias)

	print G + "OK for this part, we will enter family information!" + W
	print B + "If you choose not to, or you are done, again, enter " + R + "quit" + W

	while True:
		fam = raw_input("Choose (or quit): " + C + "\n[1]Mother\n[2]Father\n[3]Sibling\n[4]Other" + W + "\n[>]")
		if fam == "quit":
			break
		elif fam == "1":
			text_file = open("Dox of %s" % name, 'a')
			text_file.write("\n\nINFORMATION OF MOTHER")
			#Name
			momname = raw_input("[>] What is the mother's " + P + "FULL NAME? " + W)
			text_file.write("\nName of Mother: %s" % momname)
			#Age
			momage = raw_input("[>] What is the mother's " + P + "AGE? " + W)
			text_file.write("\nAge of Mother: %s" % momage)
			#DOB
			dobmom = raw_input("[>] What is the mother's " + P + "DATE OF BIRTH? " + W + "(month/day/year): ")
			text_file.write("\nDate of Birth of Mother: %s" % dobmom)
			#Aliases
			momfacebook = raw_input("[>] What about " + P + "Facebook? " + W + "Please give a link! ")
			text_file.write("\nFacebook of Mother: %s" % momfacebook)
			momtwitter = raw_input("[>] Got " + P + "Twitter? " + W + "Please give a link! ")
			text_file.write("\nTwitter of Mother: %s" % momtwitter)

			print G + "What other aliases, if available? Again, enter " + R + "quit" + W + "to exit."
			while True:
				momalias = raw_input("[>]")
				if momalias == "quit":
					break
				else:
					text_file = open("Dox of %s" % name, 'a')
					text_file.write("\n%s" % momalias)
			print "Any other members?"

		elif fam == "2":
			text_file = open("Dox of %s" % name, 'a')
			text_file.write("\n\nINFORMATION OF FATHER")
			#Name
			dadname = raw_input("[>] What is the father's " + P + "FULL NAME? " + W)
			text_file.write("\nName of Father: %s" % dadname)
			#Age
			dadage = raw_input("[>] What is the father's " + P + "AGE? " + W)
			text_file.write("\nAge of Father: %s" % dadage)
			#DOB
			dobdad = raw_input("[>] What is the father's " + P + "DATE OF BIRTH? " + W + "(month/day/year): ")
			text_file.write("\nDate of Birth of Father: %s" % dobdad)
			#Aliases
			dadfacebook = raw_input("[>] What about " + P + "Facebook? " + W + "Please give a link! ")
			text_file.write("\nFacebook of Father: %s" % dadfacebook)
			dadtwitter = raw_input("[>] Got " + P + "Twitter? " + W + "Please give a link! ")
			text_file.write("\nTwitter of Father: %s" % dadtwitter)

			print G + "What other aliases, if available? Again, enter " + R + "quit " + W + "to exit."
			while True:
				dadalias = raw_input("[>]")
				if dadalias == "quit":
					break
				else:
					text_file = open("Dox of %s" % name, 'a')
					text_file.write("\n%s" % dadalias)
			print "Any other members?"

		elif fam == "3":
			text_file = open("Dox of %s" % name, 'a')
			text_file.write("\n\nINFORMATION OF SIBLING")
			#Name
			sibname = raw_input("[>] What is the sibling's " + P + "FULL NAME? " + W)
			text_file.write("\nName of Sibling: %s" % sibname)
			#Relationship
			sibrel = raw_input("[>] What is the sibling's " + P + "RELATIONSHIP " +  W + "to the victim? ")
			text_file.write("\nRelationship to Victim: %s" % sibrel)
			#Age
			sibage = raw_input("[>] What is the sibling's " + P + "AGE? " + W)
			text_file.write("\nAge of Sibling: %s" % sibage)
			#DOB
			dobsib = raw_input("[>] What is the sibling's " + P + "DATE OF BIRTH? " + W + "(month/day/year): ")
			text_file.write("\nDate of Birth of Sibling: %s" % dobsib)
			#Aliases
			sibfacebook = raw_input("[>] What about " + P + "Facebook? " + W + "Please give a link! ")
			text_file.write("\nFacebook of Sibling: %s" % sibfacebook)
			sibtwitter = raw_input("[>] Got " + P + "Twitter? " + W + "Please give a link! ")
			text_file.write("\nTwitter of Sibling: %s" % sibtwitter)

			print G + "What other aliases, if available? Again, enter " + R + "quit " + W + "to exit."
			while True:
				sibalias = raw_input("[>]")
				if sibalias == "quit":
					break
				else:
					text_file = open("Dox of %s" % name, 'a')
					text_file.write("\n%s" % sibalias)
			print "Any other members?"

		elif fam == "4":
			text_file = open("Dox of %s" % name, 'a')
			relofother = raw_input("[>] What is the relationship of this person to the vicim? ")
			text_file.write("\n\nINFORMATION OF %s" % relofother)
			#Name
			othername = raw_input("[>] What is the person's " + P + "FULL NAME? " + W)
			text_file.write("\nName of Person: %s" % othername)
			#Age
			otherage = raw_input("[>] What is the person's " + P + "AGE? " + W)
			text_file.write("\nAge of Person: %s" % otherage)
			#DOB
			dobother = raw_input("[>] What is the person's " + P + "DATE OF BIRTH? " + W + "(month/day/year): ")
			text_file.write("\nDate of Birth of Person: %s" % dobother)
			#Aliases
			otherfacebook = raw_input("[>] What about " + P + "Facebook? " + W + "Please give a link! ")
			text_file.write("\nFacebook of Person: %s" % otherfacebook)
			othertwitter = raw_input("[>] Got " + P + "Twitter? " + W + "Please give a link! ")
			text_file.write("\nTwitter of Person: %s" % othertwitter)

			print G + "What other aliases, if available? Again, enter " + R + "quit " + W + "to exit."
			while True:
				otheralias = raw_input("[>]")
				if otheralias == "quit":
					break
				else:
					text_file = open("Dox of %s" % name, 'a')
					text_file.write("\n%s" % otheralias)
			print "Any other members?"

	print G + "OK, *whew* that was A LOT!" + W
	print C + "Now, do you have any pictures or screenshots?" + W
	while True:
		pic = raw_input("\n[>] Paste the link here. Else, " + R + "quit: " + W)
		if pic == "quit":
			break
		else:
			text_file = open("Dox of %s" % name, 'a')
			text_file.write("\nPictures/Screenshots: %s" % pic)
	print "=========================================================="
	print G + "That's it! Your D0x is complete. Check the folder where this program is contained." + W
	print "=========================================================="

########################################################################################################################################################

#Function for CUPP
def cupp():
	try:
		call(["chmod", "a+x", "cupp.py"])
		print C + "----------------------------------------------------------------"
		print "CUPP, or Common User Password Profiler, creates wordlists based"
		print "on give information of a victim"
		print "----------------------------------------------------------------" + W
		print "Loading..."
		time.sleep(3)
		call(["./cupp.py","-i"])
	except OSError:
		help = input(R +"Something is missing. Consult Help? (y/n) " + W)
		if help == "y":
			call(["gedit", "help.txt"])
		elif help == "n":
			sys.exit()

########################################################################################################################################################

#Function for theHarvester
def harvester():
	try:
		print C + "----------------------------------------------------------------"
		print "TheHarvester is a Python script that utilizes popular search"
		print "engines in order to pull out information of a specific target"
		print "----------------------------------------------------------------" + W
		print "Loading..."
		time.sleep(3)
		call(["./autoharvest.sh"])
	except OSError:
		help = input(R + "Something is missing. Consult Help? (y/n) " + W)
		if help == "y":
			call(["gedit", "help.txt"])
		elif help == "n":
			sys.exit()

########################################################################################################################################################

#Function for NMap
def nmap():
	try:
		call(["chmod", "a+x", "autonmap.py"])
		print C + "----------------------------------------------------------------"
		print "NMap is an open-source tool for network exploration and security"
		print "auditing. It is used to scan networks and systems"
		print "----------------------------------------------------------------" + W
		print "Loading..."
		time.sleep(3)
		call(["python", "autonmap.py"])
	except OSError:
		help = input(R + "Something is missing. Consult Help? (y/n) " + W)
		if help == "y":
			call(["gedit", "help.txt"])
		elif help == "n":
			sys.exit()

########################################################################################################################################################

#Function for GeoIP
def geoip():
	print C + "----------------------------------------------------------------"
	print "MaxMind has provided a module that enables a user to conduct GeoIP reconaissance."
	print "Users are able to find location data based on a IPv4 address"
	print "----------------------------------------------------------------" + W
	print "Loading..."
	time.sleep(3)
	location = raw_input("[>] What is the IP address? " )
	try:
		match = geolite2.lookup(location)
		print O + "========================================"
		gi = GeoIP.open("GeoLiteCity.dat", GeoIP.GEOIP_INDEX_CACHE | GeoIP.GEOIP_CHECK_CACHE)
		print "Collected: " + str(gi.record_by_name(location))
		print "========================================" + W

		geoiptext = raw_input("[>] Would you like this saved to a text file? (Y/N) ")
		if geoiptext == "y":
			text_file = open("geoip_information", 'a')
			text_file.write("GeoIP Information Results ")
			text_file.write("\nIP Address: %s " % location)
			text_file.write("\n" + str(gi.record_by_name(location)))
		elif geoiptext == "n":
			sys.exit(G + "Have a great one!" + W)
	except ValueError:
		print R + "That was not a valid IP Address! Care to try again?" + W
		geoip()

########################################################################################################################################################

# Function for Extractor
def webextract():
	print C + "----------------------------------------------------------------"
	print "This feature enables the user to look at a website and obtain specified"
	print "information, such as emails and phone numbers." + R + " Currently experimental!" + C
	print "----------------------------------------------------------------" + W
	print "Loading..."
	time.sleep(3)
	url = raw_input("[>] Enter the URL of the website you wish to extract information from: ")
	htmlFile = urllib.urlopen(url)
	html = htmlFile.read()
	print G + "[1] Email Addresses"
	print "[2] Phone Numbers"
	print "...more coming soon!" + C
	respin = raw_input("[>] What do you wish to extract from the site? " + W)
	if respin == '1':
		emailRegex = re.findall(r'[\w\.-]+@[\w\.-]+', html)
		print emailRegex
		emailtext = raw_input(B + "[>] Would you like it to be saved in a text file? (y/n) ")
		if emailtext == 'y':
			text_file = open("emailresult", 'a')
			text_file.write(str(emailRegex))
			print P + "Saved! Check folder this program is stored in." + W
			emaildone = raw_input("Press" + B + " Enter " + W + "when finished ")
			#Go back to main menu
			if emaildone == "":
				print ''
			else:
				print 'Why no press enter?'
		# Do NOT save to a file -> go back.
		elif emailtext == 'n':
			webextract()

	elif respin == '2':
		phoneRegex = re.findall(r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$', html)
		print phoneRegex
		phonetext = raw_input("[>] Would you like it to be saved in a text file? (y/n) ")
		if phonetext == 'y':
			text_file = open("phoneresult", 'a')
			text_file.write(str(emailRegex))
			print P + "Saved! Check folder this program is stored in." + W
			phonedone = raw_input("Press" + B + " Enter " + W + "when finished ")
			#Go back to main menu
			if phonedone == "":
				print ''
			else:
				print 'Why no press enter?'
		elif phonetext == 'n':
			webextract()

########################################################################################################################################################

def massmail():
	print C + "For this to work, make to sure to create a different email from your regular account." + W
	print "Gmail - \'smtp.gmail.com\'"
	print "Hotmail/Outlook - \'smtp-mail.outlook.com\'"
	print "Yahoo Mail - \'smtp.mail.yahoo.com\'"
	print "AT&T - \'smtp.mail.att.net\'"
	print "Comcast - \'smtp.verizon.net\'"

	smtpser = raw_input(G + "[>} What is the SMTP provider of the email account (e.g smtp.xxxx.com)? " )


	# Connect to mail server (TLS)
	smtpObj = smtplib.SMTP(str(smtpser), 587)
	smtpObj.set_debuglevel(1)
	# Test connection with message
	smtpObj.ehlo()
	# Start TLS encryption
	smtpObj.starttls()
	email_address = raw_input("[>] Enter Email Address (example@example.com): ")
	email_password = getpass("[>] Enter Email Password (will not be echoed): ")
	smtpObj.login(str(email_address), str(email_password))

	# The actual message and recipents
	recipients_address = raw_input("[>] Enter recipent addresses (seperate with comma: example@example.com, example2@example.com): ")
	recipient_list = recipients_address.split()

	body = raw_input("""[>] Write your body here. '\n' for newline. """)
	message = MIMEText("""%s""" % body)
	message['Subject'] = raw_input("[>] Write your subject here:\n")
	message['From'] = email_address
	message['To'] = ", ".join(recipient_list)
	# Sending the email
	smtpObj.sendmail(email_address, recipient_list, str(message))

########################################################################################################################################################

while True:
	print G +" ========================================"
	print O +"	 _____   ___       _   __ _   "
	print" 	|  __ \ / _ \     | | /_ | |  "
	print" 	| |  | | | | |__ _| | _| | |_ "
	print" 	| |  | | | | \ \/ / |/ / | __|"
	print" 	| |__| | |_| |>  <|   <| | |_ "
	print" 	|_____/ \___//_/\_\_|\_\_|\__|"
	print"								  "
	print B + "	     Written By: ex0dus	  " + G
	print" ======================================== " + W


	print "You are currently using " + P + str(platform.system()) + " " + str(platform.release()) + W
	if str(platform.system()) != "Linux":
		print R + "You are not using Linux. It is the recommended operating system for this program. Some features may not work" + W
	else:
		print C + "D0xk1t v2.0 nightly" + W

	print P + "NOTE: This version of D0xk1t, v2 is still in the works. Right now, you have obtained an experimental copy." + W
	print "				  "
	print "[1] Write a D0x"
	print "[2] Create a Wordlist using CUPP"
	print "[3] Harvest Information"
	print "[4] AutoNMap Menu"
	print "[5] GeoIP"
	print "[6] Website Extractor"
	print "[7] Mass Mailer"
	print "[8] What is this?"
	option = input(O +"[>] What do you want today? " + W)

	if option == 1:
		dox()
	elif option == 2:
		cupp()
	elif option == 3:
		harvester()
	elif option == 4:
		nmap()
	elif option == 5:
		geoip()
	elif option == 6:
		webextract()
	elif option == 7:
		massmail()
	elif option == 8:
		print  GR + "===================================================================================================================="
		print "Hello and welcome to D0xk1t. This is a tool I've created in python for the sole purpose of writing a D0x."
		print "In the world of hacking, D0xing is viewed as script-kiddish AND illegal and harmful."
		print "People often look down at those who write D0x. However, this tool is created not to harm."
		print "Instead, it allows hackers and hacktivists to be able to practice their reconaissance and allow themselves and others to"
		print "better protect themselves by not exposing too much of their information on the Internet."
		print" ====================================================================================================================" + W
		helpdone = raw_input("Press" + B + " Enter " + W + "when finished ")
		if helpdone == "":
			print ''
		else:
			print 'Why no press enter?'
