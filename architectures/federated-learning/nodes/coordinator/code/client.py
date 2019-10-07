import requests
import json

class Client:


	@staticmethod
	def push_finish(address):
		endpoint = "http://" + address + "/finish"
		r = requests.get(endpoint)


	@staticmethod
	def push_task(address,aggregator,model,operation,args):
		endpoint = "http://" + address + "/execute"
		payload = { 'aggregator': aggregator, 'operation': operation, 'args': args }
		files = {
			'file': model,
			'json': (None, json.dumps(payload), 'application/json'),
		}
		r = requests.post(endpoint, files=files)