from classes.aged_model import AgedModel
from classes.data_lake import DataLake
from keras.models import load_model
import numpy as np
import copy
import random
from threading import Lock
import os


class ModelRepository:


	def __init__(self,logger,train_data,test_data):
		self.max_size = 10
		self.logger = logger
		self.aged_models = []
		self.aged_models.append(AgedModel())
		self.aged_models[0].train(train_data)
		self.last_model = self.aged_models[0]
		self.test(test_data)


	def load(self,exported_model,age,train_data,test_data):
		aged_model = AgedModel(exported_model, age)
		self.aged_models.append(self.create_model_mu(aged_model, self.last_model, train_data))
		self.last_model = aged_model
		self.aged_models.sort(reverse=True, key=lambda x: x.age)
		if self.max_size + 1 == len(self.aged_models):
			self.aged_models.pop()
		self.test(test_data)


	def get_freshest_model(self):
		return self.aged_models[-1]


	# JUST FOR TESTING PURPOSES
	def test(self,data):
		test_data, test_label = data

		results = []
		for model in self.aged_models:
			results.append(model.test(data))
		self.logger.log_single_test(results)

		voted_correct = 0
		container = np.empty((1,60,4))
		for i in range(len(test_data)):
			container[0] = test_data[i]
			prediction = self.voted_predict(container)
			if prediction == np.argmax(test_label[i]):
				voted_correct += 1
		self.logger.log_voted_test(str(voted_correct / 100))


	def predict(self,data):
		return np.argmax(self.aged_models[0].predict(data))


	def voted_predict(self,data):
		result = {0: 0, 1: 0, 2: 0}
		majority_value = 0
		majority_key = 0
		for aged_model in self.aged_models:
			prediction = np.argmax(aged_model.predict(data)[0])
			result[prediction] += 1
		for k,v in result.items():
			if v > majority_value:
				majority_value = v
				majority_key = k
		return majority_key


	def update(self,aged_model,data):
		aged_model.train(data)
		# age + 1
		return aged_model


	def merge(self,aged_model1,aged_model2):
		result_age = None
		result_weights = None
		if aged_model1.age >= aged_model2.age:
			result_age = aged_model1.age
		else:
			result_age = aged_model2.age
		result_weights = np.divide(np.add(aged_model1.get_weights(), aged_model2.get_weights()), 2)
		result_model = AgedModel()
		result_model.set_weights(result_weights)
		# result_model.age = result_age
		return result_model


	def create_model_um(self,aged_model1, aged_model2,data):
		return self.merge(self.update(aged_model1, data),self.update(aged_model2, data))


	def create_model_mu(self,aged_model1, aged_model2,data):
		return self.update(self.merge(aged_model1, aged_model2), data)