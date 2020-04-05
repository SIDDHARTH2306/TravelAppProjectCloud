from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from flask_pymongo import PyMongo
import datetime
import json
import os

browse = Flask(__name__)

browse.config['MONGO_URI'] = "mongodb://54.161.172.13:27017/p_db"
browse.config['MONGO_DBNAME'] = "p_db"
mongo = PyMongo(browse)
p_db = mongo.db

@browse.route('/', methods=['GET','POST'])
def index():
	return render_template('destination.html')

@browse.route('/browse', methods = ['GET', 'POST'])
def browse_places():
	province = request.args.get('province')
	places = p_db["PlaceDetails"]
	places_fetch = places.find({"province":province})

	places_dict = {}
	counter=1
	for i in places_fetch:
		c = i.get('place_id')
		i['_id'] = c
		places_dict[c]=i
		counter+=1

	places_output = {}
	for i in places_dict:
		places_output[places_dict[i].get('name')] = places_dict[i].get('airport')
		places_output["city"] = places_dict[i].get('city')
	return render_template('destination.html', places_output=places_output)

@browse.route('/api/browse', methods=['POST', 'GET'])
def browse_places_api():
	places = p_db["PlaceDetails"]
	province = request.args.get("province")
	print(province)
	places_fetch = places.find({"province":province})
	# for i in places_fetch:
	# 	print(i)
	# 	print("asonff")
	places_dict = {}
	falgun = []
	counter=1
	for i in places_fetch:
		c = i.get('place_id')
		i['_id'] = c
		places_dict[c]=i
		falgun.append(i)
		counter+=1
	print(places_dict)
	
# return "oi"
	return jsonify(falgun)

if __name__ == '__main__':
	browse.run(host='0.0.0.0',port=5002,debug=True)


	# for i in dict:
	#	print(dict[i])
