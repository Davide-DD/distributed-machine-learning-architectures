from flask import Flask, request
from keras.models import *
from classes.model import Model
from classes.data_lake import DataLake
import os
import json
from client import Client
import sys
from classes.logger import Logger


correct = 0
wrong = 0

dl = DataLake()
model = Model()
logger = Logger()

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('[Usage] {} <process_port>'.format(sys.argv[0]))
		exit(0)
	port = int(sys.argv[1])
	app = Flask(__name__)


@app.route("/execute", methods=['POST'])
def execute():
	response = request.get_json()

	file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'my_model.h5')
	exported_model = request.files['file']
	exported_model.save(file_path)
	model.load(file_path)

	fl_plan = json.loads(request.form['json'])
	aggregator = fl_plan['aggregator']
	operation = fl_plan['operation']
	args = fl_plan['args']

	if operation == 'train':
		delta, examples_number = model.train(dl.get_training_data(), args)
		delta_json = []
		for w in delta:
			delta_json.append(w.tolist())
		result = {'delta': delta_json, 'examples_number': examples_number}

	else:
		result = model.evaluate(dl.get_training_data(), args)

	logger.log_test(model.evaluate(dl.get_test_data(), {})['evaluation'])

	print('Sono ' + str(port) + ' e sto contattando aggregator')

	Client.push_result(aggregator, operation, result)

	return 'ok'


@app.route("/predict", methods=['POST'])
def predict():
	response = request.get_json()
	data = response['TS1'], response['TS2'], response['TS3'], response['TS4']
	outcome = response['outcome']
	
	prediction = model.predict(dl.transform(data))
	print("La predizione e' " + prediction + " e il valore e' " + outcome.split()[0])
	if (outcome.split()[0] == prediction):
		global correct
		correct += 1
	else:
		global wrong
		wrong += 1
	print("Corretti: " + str(correct))
	print("Sbagliati: " + str(wrong))	

	return prediction


app.run(host='0.0.0.0',port=port)