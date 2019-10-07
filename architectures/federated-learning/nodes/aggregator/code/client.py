import requests
import json

class Client:


	@staticmethod
	def push_aggregated_result(address,operation,result,number):
		endpoint = "http://" + address + "/aggregate"
		payload = { 'operation': operation, 'result': result, 'number': number }
		r = requests.post(endpoint, json=payload)