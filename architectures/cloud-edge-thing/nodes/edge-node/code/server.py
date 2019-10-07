from flask import Flask, request
from keras.models import *
from classes.model import Model
from classes.transform import Transform
import os
import json
from client import Client
import sys


cloud_address = ''

correct = 0
wrong = 0

transform = Transform()
model = Model()

app = Flask(__name__)


@app.route("/configure", methods=['POST'])
def configure():
	fileName = 'my_model.h5'
	exported_model = request.files['file']
	exported_model.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), fileName))
	model.load(fileName)

	data = json.loads(request.form['json'])
	transform.load(data['params'][0], data['params'][1])
	global cloud_address
	cloud_address = 'http://' + request.remote_addr + ':5000'
	return 'ok'


@app.route("/predict", methods=['POST'])
def predict():
	response = request.get_json()
	dict_data = {'TS1': response['TS1'], 'TS2': response['TS2'], 'TS3': response['TS3'], 'TS4': response['TS4'] }
	data = response['TS1'], response['TS2'], response['TS3'], response['TS4']
	outcome = response['outcome']
	
	prediction = model.predict(transform.transform(data))
	print("La predizione e' " + prediction + " e il valore e' " + outcome.split()[0])
	if (outcome.split()[0] == prediction):
		global correct
		correct += 1
	else:
		global wrong
		wrong += 1
	print("Corretti: " + str(correct))
	print("Sbagliati: " + str(wrong))	

	Client.push_data(cloud_address, dict_data, outcome, prediction != outcome.split()[0])

	return prediction


app.run(host='0.0.0.0')