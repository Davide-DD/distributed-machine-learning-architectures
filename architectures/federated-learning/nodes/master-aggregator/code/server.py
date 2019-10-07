from flask import Flask, request
import numpy as np
from client import Client
import sys
from threading import Lock


coordinator_address = ''

number_of_aggregators = 0

received_weights = []

received_examples_number = []

received_evals = []

received_nodes_number = []

lock = Lock()

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print('[Usage] {} <number_of_aggregators natural coordinator ip:port process_port>'.format(sys.argv[0]))
		exit(0)
	number_of_aggregators = int(sys.argv[1])
	coordinator_address = sys.argv[2]
	port = int(sys.argv[3])
	app = Flask(__name__)


@app.route("/aggregate", methods=['POST'])
def aggregate():
	response = request.get_json()

	if response['operation'] == 'train':
		weights = response['result']
		examples_number = response['number']

		lock.acquire()
		global received_weights
		received_weights.append(weights)

		global received_examples_number
		received_examples_number.append(examples_number)

		if len(received_weights) == number_of_aggregators:
			result_weights = 0
			result_examples_number = 0

			for w in received_weights:
				if result_weights == 0:
					result_weights = w
				else:
					for i in range(0, len(result_weights)):
						result_weights[i] = np.add(np.asarray(result_weights[i]), np.asarray(w[i]))

			for n in received_examples_number:
				result_examples_number = result_examples_number + n

			received_weights.clear()
			received_examples_number.clear()

			for i in range(0, len(result_weights)):
				result_weights[i] = np.divide(result_weights[i], result_examples_number).tolist()

			Client.push_result(coordinator_address, result_weights)
		lock.release()

	else: # Allora l'operazione richiesta e' evaluate
		evaluation = response['result']
		nodes_number = response['number']

		lock.acquire()

		global received_evals
		received_evals.append(evaluation)

		global received_nodes_number
		received_nodes_number.append(nodes_number)

		if len(received_evals) == number_of_aggregators:
			result_evals = 0
			result_numbers = 0
			for e in received_evals:
				result_evals = result_evals + e
			for n in received_nodes_number:
				result_numbers = result_numbers + n
			result = result_evals / result_numbers
			received_evals.clear()
			received_nodes_number.clear()
			Client.push_result(coordinator_address, result)

		lock.release()

	return 'ok'


app.run(host='0.0.0.0',port=port)