from flask import Flask, flash, render_template, request, redirect,jsonify
from werkzeug import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import pymongo
import csv
import cPickle as cp
from helper import *
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


with open('routes_final.pkl','rb') as f: #routes_final is updated version
	route_dict = cp.load(f)
print 'static data loaded'

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/submit',methods=['POST'])
def results():
	#try:
		if request.method == 'POST':
			form = request.form
			print form
			form = dict(form)
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
			print request.environ['REMOTE_ADDR']
			form['ip'] = request.remote_addr
			dump_to_mongo(form)
			return jsonify(form)
	#except:
		#return "<center> <h5> Error 404 <h5> <center> "

@app.route('/all',methods=['GET'])
def all():
	try:
		if request.method == 'GET':
			return jsonify(route_dict.keys())
	except:
		return jsonify({'no':'places'})

@app.route('/admin',methods=['GET','POST'])
def admin():
	#try:
		if request.method == 'GET':
			data = list(collection.find())
			headers = ['from', 'to','time','date','adults','children', 'fname','lname','oCountry','email','phone','ip','time_of_entry','_id','flight','passport']

			with open('admin.csv','wb') as fou:
				dw = csv.DictWriter(fou,delimiter='\t',fieldnames=headers)
				dw.writeheader()
				for i in data:
					dw.writerow(i)
			return "csv file created"
	#except:
		#return jsonify({'error':'error'})

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
			result = route_dict[query]
			return jsonify(result)
	except:
		return jsonify({'error':'error'})



if __name__ == "__main__":
	app.run(debug=True, port=8080)#,threaded=True)
