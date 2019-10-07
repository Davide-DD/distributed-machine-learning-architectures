from flask import Flask, request
from classes.data_lake import DataLake
from classes.model import Model
from classes.policy import Policy
from client import Client
import sys


edge_address = ""

dl = DataLake()

model = Model()
model.train(dl.get_training_data())

policy = Policy()


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('[Usage] {} <edge ip:port>'.format(sys.argv[0]))
		exit(0)
	edge_address = sys.argv[1]
	Client.push_model(edge_address, model.export(), dl.get_transform_params())
	app = Flask(__name__)


@app.route("/update", methods=['POST'])
def update():
	content = request.get_json()
	data = {'TS1': content['data']['TS1'], 'TS2': content['data']['TS2'], 'TS3': content['data']['TS3'], 'TS4': content['data']['TS4']}
	outcome = content['outcome']

	dl.add_data(data, outcome)
	
	if content['wrong_prediction'] == True:
		policy.update_status()

		if not policy.is_respected():
			dl.load_data()
			model.train(dl.get_training_data())
			Client.push_model(edge_address, model.export(), dl.get_transform_params())

	return 'ok'


app.run(host='0.0.0.0')
