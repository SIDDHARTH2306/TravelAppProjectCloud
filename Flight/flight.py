from flask import Flask, render_template, request, redirect, jsonify, session
from flask_restful import Resource, reqparse
from flask_pymongo import PyMongo
from pymongo import MongoClient
import datetime
import json
import os
import pprint


flight = Flask(__name__)
flight.secret_key = 'mysecret'

flight.config['MONGO_URI'] = "mongodb://54.236.253.176:27017/p_db"
flight.config['MONGO_DBNAME'] = "p_db"
mongo = PyMongo(flight)
p_db = mongo.db

@flight.route('/<city_name>', methods=['GET'])
def main(city_name):
	city_name = city_name
	session['city'] = city_name
	return render_template('flights.html', city_name=city_name)

@flight.route('/show_flights', methods=['GET','POST'])
def show_flights():
	# return render_template('flights.html')
	source = request.form.get("source")

	print(source)

	flight = p_db["FlightDetails"]
	flight_query_fetch = flight.find({"departure_plc":source})
	# print(flight_query_fetch)
	# , "destination":destination})
	# for i in flight_query_fetch:
	# 	print(i)
	# 	print("kk")

	flight_dic = {}
	counter=1
	for i in flight_query_fetch:
		c = i.get('flightcode')
		# print("Hi")
		i['_id'] = c
		# print(c)
		flight_dic[c]=i
		counter+=1

	flight_list = [flight_dic[i] for i in flight_dic]
	print(flight_list)
	# flights = travel_app["flights"]
	# flight_fetch = flights.find()
	# flight_dic = {}
	# counter=1
	# for i in flight_fetch:
	# 	c = i.get('code')
	# 	i['_id'] = counter
	# 	flight_dic[c]=i
	# 	counter+=1

	# return "oi"
	return render_template("flights.html", flight_list=flight_list, session=session)


@flight.route('/api/flight', methods=['GET','POST'])
def api_flights():
	source = request.args.get("source")
	destination = request.args.get("destination")
	flight = p_db["FlightDetails"]
	flight_query_fetch = flight.find({"departure_plc":source,"destination_plc":destination})
	# , "destination":destination})
#	for i in flight_query_fetch:
#		print(i)

	flight_dic = {}
	counter=1
	for i in flight_query_fetch:
		c = i.get('flightcode')
		# print("Hi")
		i['_id'] = c
		# print(c)
		flight_dic[c]=i
		#falgun_flight.append(i)
		counter+=1
	
	flight_list = [flight_dic[i] for i in flight_dic]
	print(flight_list)

	# print(counter)
	# print(flight_dic)
	# return "oi"
	return jsonify(flight_list)


# class FlightList(Resource):



if __name__== "__main__":
	flight.run(host='0.0.0.0',port=5001,debug=True)