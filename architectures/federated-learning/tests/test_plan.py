import subprocess
import requests
import time
import os
import sys


if len(sys.argv) < 2:
	print('[Usage] {} <test_architecture_name> <aggregators_number>'.format(sys.argv[0]))
	exit(0)


aggregators_number = int(sys.argv[2])
aggregators_addresses = []
for i in range(0,aggregators_number):
	if i < 10:
		aggregators_addresses.append('192.168.0.148:530' + str(i))
	else:
		aggregators_addresses.append('192.168.0.148:53' + str(i))

killer_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_killer.sh')
executor_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_executor.py')

subprocess.call([killer_path])
time.sleep(5)

subprocess.call(['python3', executor_path, sys.argv[1]])
time.sleep(60)

epochs_per_round = 5
for j in range(0,400):
	if j % 2 > 0:
		initial_epoch = (j // 2) * epochs_per_round
		destination_epoch = initial_epoch + epochs_per_round
		data = {
			"operation": "train",
			"aggregators": aggregators_addresses,
			"args": {
				"initial_epoch": initial_epoch,
				"epochs": destination_epoch,
				"shuffle": "False",
				"batch_size": 3
			}
		}
		seconds = 200
	else:
		data = {
			"operation": "evaluate",
			"aggregators": aggregators_addresses,
			"args": {
				"batch_size": 3
			}
		}
		seconds = 30
	requests.post('http://192.168.0.148:5100/start', json=data)
	time.sleep(seconds)