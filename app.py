from flask import Flask, flash, render_template, request, redirect,jsonify,send_file
from werkzeug import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import pymongo
import csv
import cPickle as cp
from helper import *
import helper
from configuration import *

KEY = '1234'
app = Flask(__name__,static_url_path='/static')
app.secret_key = KEY


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = SENDER_MAIL #ADMINS EMAIL
app.config['MAIL_PASSWORD'] = SENDER_PASSWORD
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail_obj = Mail(app)

route_dict['bandaranaike international airport'] = route_dict['bia']


@app.route('/')
def home():
	return render_template('index.html')

@app.route('/submit',methods=['POST'])
def results():
	try:
		if request.method == 'POST':
			form = request.form
			form = dict(form)
			for k in form.keys():
				form[k] = form[k][0].encode('ascii')
			print form
			#form_dict['from'] = form['from']
			#form_dict['to'] = form['to']
			#form_dict['time'] = str(form['time'])
			#form_dict['date'] = str(form['date'])
			#form_dict['adults'] = str(form['adults'])
			#form_dict['children'] = str(form['children'])
			#form_dict['fname'] = str(form['fname'])
			#form_dict['lname'] = str(form['lname'])
			#form_dict['email'] = str(form['email'])
			#form_dict['phone'] = str(form['phone'])
			#form_dict['passport'] = str(form['passport'])
			#form_dict['oCountry'] = str(form['oCountry'])
			#form_dict['flight'] = str(form['flight'])
			#form_dict['ip'] = request.remote_addr
			#print request.environ['REMOTE_ADDR']
			form['ip'] = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
			#form['ip'] = request.remote_addr
			helper.dump_to_mongo(form)
			if ( ( (form['from'] == 'bia') or (form['from'] == 'bandaranaike international airport'))  and ( (form['to']=='galle') or (form['to']=='hikaduwa'))):
				#helper.dump_to_mongo(form)
				print 'sending mail'
				if helper.send_email_sms(form,mail_obj):
					print 'DONE,mail sent'
				return jsonify({'success':'true'})
			return jsonify({'success':'false'})
	except:
		return "<center> <h5> Error 404 <h5> <center> "

@app.route('/all',methods=['GET'])
def all():
	try:
		if request.method == 'GET':
			keys = route_dict.keys()
			#keys.remove('bia')
			#keys.append('bandaranaike international airport')
			return jsonify(keys)
	except:
		return jsonify({'no':'places'})

@app.route('/admin',methods=['GET','POST'])
def admin():
	try:
		if request.method == 'GET':
			return render_template('admin.html')

		if request.method == 'POST':
			form = request.form
			if form['password'] == 'creathives123':
				data = list(collection.find())
				print data
				#headers = ['from', 'to','time','date','adults','fname','lname','oCountry','email','phone','ip','time_of_entry','_id','flight','passport']
				headers = data[0].keys()
				with open('admin.csv','wb') as fou:
					dw = csv.DictWriter(fou,delimiter='\t',fieldnames=headers)
					dw.writeheader()
					for i in data:
						dw.writerow(i)
				print "csv file created"
			        return send_file('admin.csv', as_attachment=True)
			else:
				return "<h1>you unauthorized PIG !!<h1>"

	except:
		return jsonify({'error':'error'})

@app.route('/places',methods = ['GET','POST'])
def places():
	try:
		if request.method == 'GET':
			query = request.args.get('from')
			query = query.upper()
			res = collection_2.find({"Orig":query},{"_id":0})
			find_results = []
			for i in res:
				find_results.append(i)
			return jsonify({'results':find_results})
	except:
		return jsonify({'error':'error'})

@app.route('/route',methods=['GET','POST'])
def routes():
	try:
		if request.method == 'GET':
			query = request.args.get('from')
			query = query.lower()
			print query

			result = defaultdict()
			"""CHAPPAR AMOGHA"""
			#result['possible_destinations'] = helper.get_all_possible_routes(query)
			destinations = []
			query_result = route_dict[query]

			route_dict['bandaranaike international airport'] = route_dict['bia']
			for i in query_result:
				destinations.append(i['name'])
			
			if 'bia' in destinations:
				destinations.append('bandaranaike international airport')

			result['query'] = route_dict[query]
			result['possible_destinations'] = list(set(destinations))
			return jsonify(result)
	except:
		return jsonify({'error':'error'})



if __name__ == "__main__":
	app.run(port=5000,host='0.0.0.0',threaded=True)

