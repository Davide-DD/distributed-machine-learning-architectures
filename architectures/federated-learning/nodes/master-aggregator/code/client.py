import requests
import json

class Client:


	@staticmethod
	def push_result(address,result):
		endpoint = "http://" + address + "/finish"
		payload = { 'result': result }
		r = requests.post(endpoint, json=payload)
