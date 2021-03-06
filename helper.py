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
from graph_functions import *
import process_data

conn = pymongo.MongoClient(MONGO_ADDRESS)              # Mongo Stuff
conn.admin.authenticate(MONGO_USERNAME, MONGO_PASSWORD)
db = conn.travel
collection = db.users
collection_2 = db.places

print 'db authenticated'

route_dict = process_data.create_route()

graph,mapping = create_graph(route_dict) #mapping maps places to numbers
inv_mapping = {v: k for k, v in mapping.iteritems()} #inverse mapping

print 'static data loaded'

def dump_to_mongo(form_dict):
	form_dict['time_of_entry'] = str(datetime.datetime.now())
	collection.insert_one(form_dict)
	print "inserted"
"""
def get_all_possible_routes(source):
	global graph
	global route_dict
	keys = route_dict.keys()
	possible_destinations = set()
	for k in keys:
		results = graph.get_all_paths(mapping[source],mapping[k])
		for res in results:
			res.remove(mapping[source])
			res = [inv_mapping[i] for i in res]
			possible_destinations.update(res)
	return list(possible_destinations)
"""

def send_email_sms(form_dict,mail_obj):
	try:
	
		customer_details = list(collection.find({"$and":[{"email":form_dict['email']},{"phone":form_dict['phone']},{"fname":form_dict['fname']}]}))[0]
		unique_id = str(customer_details['_id'])
		message = """\tYour unique booking id is : %s
					\tName : Mr %s,
					\tFrom: %s
					\tDestination: %s
				 	\tDate : %s
					\tTime : %s
					\tSeats:%s
					\t fare :%s
					\t Contact number:+94773161935
					\t Email :info.lankanmayil@gmail.com
				"""%(unique_id,form_dict['fname'],form_dict['from'],form_dict['to'],form_dict['date'],form_dict['time'],form_dict['adults'],form_dict['rupee'])

		print "sending to admin.."
		message = "\tYou have received a booking!\n" + message
		msg = Message('Booking Alert', sender = SENDER_MAIL, recipients = [ADMIN_MAIL])
		msg.html = message
		mail_obj.send(msg)
		print "email sent to admin"
		print "Sending SMS to admin"
		send_sms(message,SMS_CLIENTS=[ADMIN_NUMBER])
		print "sms sent to admin"

		print "sending to Customer.."
		#message = " <h1>Booking Details </h1>" + message


		#current_route = route_dict[form_dict['from']]
		#print current_route
		#fare_rupee = list(i['rupee'] for i in current_route if i['name'] == form_dict['to'])[0]
		#fare_usd = list(i['usd'] for i in current_route if i['name'] == form_dict['to'])[0]
		fare_rupee = 2500
		fare_usd = 17
		#seats = int(form_dict['adults'])
		#fare_msg = "USD: "+str(fare_usd*seats) + "  LKR: "+str(fare_rupee*seats)
		
		#if seats >= 4:
		#	fare_msg = "USD: "+str(fare_usd*seats-(3.5*(seats-3))) + "  LKR: "+str(fare_rupee*seats-(500*(seats-3)))			
		
		message = """<html>
                             <body>
			     <center> <a href=\"http://www.dumpt.com/img/viewer.php?file=s6j2mcg3rt3psevb4pi2.jpg\" target=\"_blank\"><img src=\"http://www.dumpt.com/img/files/s6j2mcg3rt3psevb4pi2_thumb.jpg\" border=\"0\" alt=\"Dumpt.com\"/></a> </center> <br>
                                <b> Dear  %s  <br>
                                Thanks for using Lankan Mayil!!  <br>
                                Your booking details are shown below.<br>
                                Your Unique Booking ID: %s <br>
                                From: %s <br>
								To : %s <br>
								Date of Travel: %s <br>
								Scheduled departure Time: %s <br>
								No of Passengers: %s <br>
								Fare per seat: %s <br>
								Total Fare: %s (inclusive of all taxes)<br>
								Contact number:+94773161935 <br>
			                                        Email :info.lankanmayil@gmail.com <br>
							<br>
							<b> Note :</b> All payments will be made in cash only.Both USD and Srilankan
										   Rupee will be accepted. Payment to be made to our agent while departure or boarding.	</b>
							
                            </body>
                    </html>"""%(form_dict['fname'],unique_id,form_dict['from'].title(),form_dict['to'].title(),form_dict['date'],form_dict['time'],form_dict['adults'],'USD: '+str(fare_usd)+"  "+'LKR: '+str(fare_rupee),form_dict['usd']+" "+form_dict['rupee'])	


		
		msg = Message('Booking Alert', sender = SENDER_MAIL, recipients = [form_dict['email']])
		msg.html = message
		mail_obj.send(msg)
		print "email sent to customer"
		#print "Sending SMS to customer"
		#send_sms(message,SMS_CLIENTS=[form_dict['phone']])
		#print "sms sent to customer"

		return True
	except:
		print "Error sending mail"
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

