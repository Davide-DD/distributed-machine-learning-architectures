import requests
import json

class Client:


	@staticmethod
	def push_model(address,exported_model,transform_params):
		endpoint = address + "/configure"
		payload = { 'params': transform_params }
		files = {
			'file': exported_model,
			'json': (None, json.dumps(payload), 'application/json'),
		}
		r = requests.post(endpoint, files=files)