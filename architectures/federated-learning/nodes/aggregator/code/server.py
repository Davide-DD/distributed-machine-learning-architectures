from flask import Flask, request
import numpy as np
from client import Client
import sys
from threading import Lock


master_aggregator_address = ''

number_of_edge_nodes = 0

received_evals = []

received_weights = []

received_examples_number = []

lock = Lock()

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print('[Usage] {} <number_of_edge_nodes natural master_aggregator ip:port process_port>'.format(sys.argv[0]))
		exit(0)
	number_of_edge_nodes = int(sys.argv[1])
	master_aggregator_address = sys.argv[2]
	port = int(sys.argv[3])
	app = Flask(__name__)


@app.route("/aggregate", methods=['POST'])
def aggregate():
	response = request.get_json()

	if response['operation'] == 'train':
		weights = response['delta']
		examples_number = response['examples_number']

		lock.acquire()
		global received_weights
		received_weights.append(weights)

		global received_examples_number
		received_examples_number.append(examples_number)

		if len(received_weights) == number_of_edge_nodes:
			result_weights = 0
			result_examples_number = 0

			for w in received_weights:
				if result_weights == 0:
					result_weights = w
				else:
					for i in range(0, len(result_weights)):
						result_weights[i] = np.add(np.asarray(result_weights[i]), np.asarray(w[i])).tolist()

			for n in received_examples_number:
				result_examples_number = result_examples_number + n
			received_weights.clear()
			received_examples_number.clear()

			print('Sono ' + str(port) + ' e sto contattando il master')
			Client.push_aggregated_result(master_aggregator_address, 'train', result_weights, result_examples_number)

		lock.release()

	else: # Allora l'operazione richiesta e' evaluate
		evaluation = response['evaluation']

		lock.acquire()
		global received_evals
		received_evals.append(evaluation)

		if len(received_evals) == number_of_edge_nodes:
			result_evals = 0
			for e in received_evals:
				result_evals = result_evals + e
			received_evals.clear()
			print('Sono ' + str(port) + ' e sto contattando il master')
			Client.push_aggregated_result(master_aggregator_address, 'evaluate', result_evals, number_of_edge_nodes)
		lock.release()
	return 'ok'


app.run(host='0.0.0.0',port=port)