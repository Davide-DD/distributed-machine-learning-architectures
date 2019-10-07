import requests



class Client:


	@staticmethod
	def push_data(address,data,outcome,wrong_prediction):
		endpoint = address + "/update"
		payload = {'data': data, 'outcome': outcome, 'wrong_prediction': wrong_prediction}
		r = requests.post(endpoint, json=payload)
		print(r.status_code)
		print(r.content)