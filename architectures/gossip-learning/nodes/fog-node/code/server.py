from classes.model_repository import ModelRepository
from classes.peer_repository import PeerRepository
from classes.data_lake import DataLake
from classes.aged_peer import AgedPeer
from client import Client
from flask import Flask, request, make_response, jsonify
import sys
import socket
import os
import json
from datetime import datetime
import signal
from threading import Lock
from classes.logger import Logger


def signal_handler(sig, frame):
	print('Terminating...')
	client.stop()
	exit(1)

signal.signal(signal.SIGINT, signal_handler)

correct = 0
wrong = 0

logger = Logger()

dl = DataLake()
train_data = dl.get_training_data()
test_data = dl.get_test_data()

mr = ModelRepository(logger,train_data,test_data)
pr = None
client = None

lock = Lock()

if __name__ == '__main__':
	peers = []
	for p in sys.argv[2:]:
		peers.append(p)
	port = sys.argv[1]
	pr = PeerRepository(9, 5, 0, socket.gethostbyname(socket.gethostname()) + ':' + port, peers, logger)
	client = Client(10, pr, mr)
	app = Flask(__name__)


@app.route("/model", methods=['POST'])
def model():
	data = json.loads(request.form['json'])

	file_name = 'my_model' + str(datetime.timestamp(datetime.now())) + '.h5'
	file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
	exported_model = request.files['file']
	exported_model.save(file_path)

	lock.acquire()
	mr.load(file_path, data['age'], train_data, test_data)
	lock.release()
	
	os.remove(file_path)

	peers = []
	for peer in json.loads(data['peers']):
		peers.append(AgedPeer.from_json(peer))
	pr.load(peers)

	return 'ok'


@app.route("/predict", methods=['POST'])
def predict():
	response = request.get_json()
	data = response['TS1'], response['TS2'], response['TS3'], response['TS4']
	outcome = response['outcome']
	
	result = mr.voted_predict(dl.transform(data))
	if result == 0:
		prediction = '3'
	elif result == 1:
		prediction = '20'
	else:
		prediction = '100'

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


app.run(host='0.0.0.0', port=int(port))