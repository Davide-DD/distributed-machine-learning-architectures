from keras.models import *
from keras.layers import *
import numpy as np
import tensorflow as tf
import os



class Model:


	def load(self,exported_model):
		self.graph = tf.Graph()
		with self.graph.as_default():
			self.session = tf.Session()
			with self.session.as_default():
				self.model = load_model(exported_model)
				self.model._make_predict_function()
		

	def train(self,data,args):
		with self.graph.as_default():
			with self.session.as_default():

				X_train, y_train = data

				initial_weights = self.model.get_weights()

				# Addestra il modello, restituendo infine un oggetto History con vari parametri che permettono di vedere come si sono evolute le performance
				# 1. numpy array o lista di numpy array (secondo la dimensionalità attesa)
				# 2. come sopra
				# 3. numero di sample da utilizzare prima di aggiornare i pesi
				# 4. numero di iterazioni da fare sui dati in input
				# 5. frazione dei dati di apprendimento da utilizzare come validazione
				# Args deve essere batch_size=32, epochs=10, shuffle=True
				self.model.fit(X_train, y_train, initial_epoch=args.get('initial_epoch', 0), steps_per_epoch=args.get('steps_per_epoch', None), batch_size=args.get('batch_size', None), epochs=args.get('epochs', 1), verbose=1, shuffle=args.get('shuffle', False))

				result_weights = np.subtract(self.model.get_weights(), initial_weights) * len(X_train)

				return result_weights, len(X_train)


	def evaluate(self,data,args):
		with self.graph.as_default():
			with self.session.as_default():

				X_train, y_train = data

				# Args deve essere vuoto
				result = self.model.evaluate(X_train, y_train, verbose=1, steps=args.get('steps', None), batch_size=args.get('batch_size', None))

				return {'evaluation': result[1]}


	def predict(self,data):
		with self.graph.as_default():
			with self.session.as_default():

				predictions = self.model.predict(data)
				result = np.where(predictions[0] == np.amax(predictions[0]))
				if result[0][0] == 0:
					return '3'
				elif result[0][0] == 1:
					return '20'
				else:
					return '100'