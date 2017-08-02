import pymongo
import datetime
import os
import sys
import urllib2
import cookielib
from getpass import getpass
from stat import *
from configuration import * #HAS ALL IMPORTANT STUFF LIKE PASSWORD AND USERNAMES
from flask_mail import Mail, Message


conn = pymongo.MongoClient(MONGO_ADDRESS)              # Mongo Stuff
conn.admin.authenticate(MONGO_USERNAME, MONGO_PASSWORD)
db = conn.travel
collection = db.users
collection_2 = db.places

print 'db authenticated'

def dump_to_mongo(form_dict):
	form_dict['time_of_entry'] = str(datetime.datetime.now())
	collection.insert_one(form_dict)
	print "inserted"

def send_email_sms(form_dict,mail_obj):
	try:
		message = """\tName : Mr %s,
					\tDestination: %s
				 	\tDate : %s
					\tTime : %s
					\tAdults:%s
					\tchildren:%s
					\t Contact number:%s
					\t Email :%s\n
				"""%(form_dict['username'],form_dict['to_selected'],form_dict['date'],form_dict['time']
				,form_dict['adults'],form_dict['children'],form_dict['phone'],form_dict['email'])

		print "sending to admin.."
		message = "\tYou have received a booking!\n" + message
		msg = Message('Booking Alert', sender = 'hjkpidiot@gmail.com', recipients = [ADMIN_MAIL])
		msg.body = message
		mail_obj.send(msg)
		print "email sent to admin"
		print "Sending SMS to admin"
		send_sms(message,SMS_CLIENTS=[ADMIN_NUMBER])
		print "sms sent to admin"

		print "sending to Customer.."
		message = "\tBooking Details\n" + message
		msg = Message('Booking Alert', sender = SENDER_MAIL, recipients = [form_dict['email']])
		msg.body = message
		mail_obj.send(msg)
		print "email sent to customer"
		#print "Sending SMS to customer"
		#send_sms(message,SMS_CLIENTS=[form_dict['phone']])
		#print "sms sent to customer"

		return True
	except:
		print "Error"
		return False

def send_sms(message,SMS_CLIENTS):

	for number in SMS_CLIENTS:
		message = "+".join(message.split(' '))
		url ='http://site24.way2sms.com/Login1.action?'
		data = 'username='+WAY2SMS_USERNAME+'&password='+WAY2SMS_PASSWORD+'&Submit=Sign+in'

	 	#For cookies
		cj= cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

	 	#Adding header details
		opener.addheaders=[('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120')]
		try:
			usock =opener.open(url, data)
		except IOError:
			print "error opening cookie jar!"

		jession_id =str(cj).split('~')[1].split(' ')[0]
		send_sms_url = 'http://site24.way2sms.com/smstoss.action?'
		send_sms_data = 'ssaction=ss&Token='+jession_id+'&mobile='+number+'&message='+message+'&msgLen=138'
		opener.addheaders=[('Referer', 'http://site25.way2sms.com/sendSMS?Token='+jession_id)]
		try:
			sms_sent_page = opener.open(send_sms_url,send_sms_data)
		except IOError:
			print "error sending sms"
			return False
		print "SMS sent"

	return True
