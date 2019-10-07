import requests



class Client:


	@staticmethod
	def push_result(address,operation,result):
		endpoint = "http://" + address + "/aggregate"
		payload = {'operation':operation}
		for k, v in result.items():
			payload[k] = v
		r = requests.post(endpoint, json=payload)
