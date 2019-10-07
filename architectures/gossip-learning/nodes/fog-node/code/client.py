import threading
import time
import requests
import json
import os


class Client:


	def __init__(self, pause, pr, mr):
		self.to_stop = False
		x = threading.Thread(target=self.__gossip_average, args=(pause, pr, mr,))
		x.start()


	def stop(self):
		self.to_stop = True


	def __send_model(self, model, age, recipient, others):
		endpoint = 'http://' + recipient.address + "/model"
		payload = { 'age': age, 'peers': json.dumps(others, default = lambda x: x.__dict__) }
		files = {
			'file': model,
			'json': (None, json.dumps(payload), 'application/json'),
		}
		try:
			r = requests.post(endpoint, files=files)
			recipient.age = 0
		except:
			print('Recipient ' + recipient.address + ' is not responding...')


	def __gossip_average(self, pause, pr, mr):
		while not self.to_stop:
			recipient, others = pr.select()
			if others:
				model = mr.get_freshest_model()
				exported_model, file_path = model.export()
				self.__send_model(exported_model, model.age, recipient, others)
				exported_model.close()
				os.remove(file_path)
			time.sleep(pause)