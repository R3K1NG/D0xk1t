''''

work in progresss

'''



#!/usr/bin/python
import sys, os, time
import nmap
from subprocess import call

print "I'm sorry, but right now, I'm working on improving features for this. I will push changes as soon as possible, so make sure to update repository."

while True:

	print "----------------------------------------------------------------"
	print " [+] NMap Automatic Network/Host Scanner [+]"
	print " By: Alan Cao"
	print "----------------------------------------------------------------"

	nm = nmap.PortScanner()
	host = raw_input("[>] What is the host you want to scan (e.g 127.0.0.1)? ")
	port = raw_input("[>] What is the port or port-ranges? ")

	print "Options:"
	print "1)Simple Scan\n2)Intense Scan\n3)IPv6 Scan\n4)Ping Scan\n5)Fast Scan\n6)UDP Scan"
	print "7)Port Selection\n8)Port Scan (TCP SYN)\n9)OS Detection Scan"
	print "10)Standard Service Detection\n11)Heartbleed SSL Vulnerability Scan\n12)IP Info\n14)Go Back"

	option = input("[>] Choose An Option, Young Padawan: ")

	if option == 1:
		print '----------------------------------------------------'
		print 'Host: %s' % host
		print 'Status: %s' %





'''
	if option == 1:
		call(["nmap", "-v", target])
	elif option == 2:
		call(["nmap", "-T4", "-A", target])
	elif option == 3:
		call(["nmap", "-6", target])
	elif option == 4:
		call(["nmap", "-sP", target])
	elif option == 5:
		call(["nmap", "-F", target])
	elif option == 6:
		call(["nmap", "-sU", target])
	elif option == 7:
		call(["nmap", "-p", target])
	elif option == 8:
		call(["nmap", "-sS", target])
	elif option == 9:
		call(["nmap", "-A", target])
	elif option == 10:
		call(["nmap", "-sV", target])
	elif option == 11:
		call(["nmap", "-sV", "-p 443", "--script=ssl-heartbleed", target])
	elif option == 12:
		call(["nmap", "--script=asn-query", "whois", "ip-geolocation-maxmind", target])
	elif option == 13:
		call(["gedit", "help.txt"])
	elif option == 14:
		call(["python","menu.py"])
'''
