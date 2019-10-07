from flask import Flask, request
from classes.model import Model
from client import Client
import sys
import threading


orchestrator_address = ''

edge_addresses = []

current_operation = ''

model = Model()


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('[Usage] {} <process_port edge_addresses+ ip:port>'.format(sys.argv[0]))
		exit(0)
	port = int(sys.argv[1])
	for address in sys.argv[2:]:
		edge_addresses.append(address)
	app = Flask(__name__)


@app.route("/start", methods=['POST'])
def start():
	global orchestrator_address, current_operation
	orchestrator_address = request.remote_addr + ':5000'

	plan = request.get_json()

	current_operation = plan['operation']

	aggregator_addresses = plan['aggregators']
	
	edge_per_aggregator = int(len(edge_addresses) / len(aggregator_addresses))

	exported_model_file = model.export()
	exported_model = exported_model_file.read()
	exported_model_file.close()

	for i in range(len(edge_addresses)):
		x = threading.Thread(target=Client.push_task, args=(edge_addresses[i], aggregator_addresses[i // edge_per_aggregator], exported_model, current_operation, plan['args']))
		x.start()

	return 'ok'


@app.route("/finish", methods=['POST'])
def finish():
	global current_operation

	request_json = request.get_json()

	if current_operation == 'train':
		model.update(request_json['result'])

	else:
		print('Accuracy: ' + str(request_json['result']))

	Client.push_finish(orchestrator_address)

	return 'ok'


app.run(host='0.0.0.0', port=port)