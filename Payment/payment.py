from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from flask_pymongo import PyMongo
import datetime
import json
import os

payment = Flask(__name__)

payment.config['MONGO_URI'] = "mongodb://54.159.158.177:27017/p_db"
payment.config['MONGO_DBNAME'] = "p_db"
mongo = PyMongo(payment)
p_db = mongo.db

@payment.route('/', methods=['GET','POST'])
def index():
	return render_template('payment.html')

@payment.route('/payment', methods = ['GET', 'POST'])
def ticket_payment():
	payment_db = mongo.db.payment

	if request.method == 'POST':
		
		email = request.form.get('email')
		fname = request.form.get('fname')
		lname = request.form.get('lname')
		credit = request.form.get('credit')
		nameoncard = request.form.get('nameoncard')
		expiry = request.form.get('expiry')
		cvv = request.form.get('cvv')

		print(email,fname,type(credit))

		if(len(credit)!=16):
			return render_template('payment.html', credit_Error= "Invalid card number")

		
		data=[]

		if(not email or not fname or not lname or not credit or not nameoncard or not expiry or not cvv):
			return render_template('payment.html', credit_Error= "Please enter all details")

		else:
			data.append(email)
			data.append(fname)
			data.append(lname)
			data.append(credit)
			data.append(nameoncard)
			data.append(expiry)
			data.append(cvv)

			fdata=list(data)

			payment_db.insert_one({'email': email, 'fname': fname, 'lname': lname, 'ticket_booked' : True})

			return render_template('booked.html',i=data)
		
	if request.method == 'GET':
		return render_template('payment.html')

if __name__ == '__main__':
	payment.run(host='0.0.0.0',port=5003,debug=True)
