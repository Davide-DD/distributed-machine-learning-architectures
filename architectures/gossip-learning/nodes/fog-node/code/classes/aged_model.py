from keras import backend as K
from keras.models import *
from keras.layers import *
import os
from datetime import datetime
import tensorflow as tf
import numpy as np


class AgedModel:


	def __init__(self, model=None, age=None):		
		self.graph = tf.Graph()

		with self.graph.as_default():

			self.session = tf.Session()

			with self.session.as_default():

				if model == None:
					n_sensors, t_periods = 4, 60

					# L'oggetto Sequential crea una pila lineare di livelli
					model = Sequential()

					# Come primo livello, aggiunge un livello di convoluzione a 1 dimensione con i seguenti argomenti: 
					# 1. Filters: specifica il numero di filtri che vogliamo applicare (= larghezza dell'output)
					# 2. Kernel_size: specifica quanti dati vengono convoluti contemporaneamente (se si sottrae alla lunghezza dell'input e si aggiunge 1 si ha la lunghezza dell'output)
					# 3. activation: funzione di attivazione dei neuroni
					# 4. input_shape: definisce la "forma" dell'input
					model.add(Conv1D(100, 6, activation='relu', input_shape=(t_periods, n_sensors)))

					# Altro livello come sopra
					model.add(Conv1D(100, 6, activation='relu'))

					# Livello di pooling per convoluzioni 1D: prende 3 input alla volta e li sostituisce con il valore massimo che trova per evitare l'overfitting
					model.add(MaxPooling1D(3))

					# Altro livello di convoluzione 1D
					model.add(Conv1D(160, 6, activation='relu'))

					# Ultimo livello di convoluzione 1D
					model.add(Conv1D(160, 6, activation='relu'))

					# Livello di pooling che computa il valore medio per ogni riga
					model.add(GlobalAveragePooling1D())

					# Non proprio un livello: serve a settare a 0 la metà (0.5) dei valori in input per ridurre l'overfitting
					model.add(Dropout(0.5))

					# Ultimo livello composto da 3 nodi con attivazione softmax, che:
					# Assegna a ogni valore in uscita dai nodi sopra un valore compreso tra 0 e 1; la somma di questi valori fa 1
					model.add(Dense(3, activation='softmax'))

					# Specifica come si esegue il processo di apprendimento dai dati, utilizzando:
					# 1. loss: funzione che si cerca di minimizzare
					# 2. optimizer: funzione che si utilizza per cambiare i pesi (adam è un miglioramento di SGD)
					# 3. metrics: lista di metriche che vuoi tenere sott'occhio durante l'apprendimento
					model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

					self.model = model

				else:
					self.model = load_model(model)

		if age != None:
			self.age = age
		else:
			self.age = datetime.timestamp(datetime.now())


	def train(self,data):
		with self.graph.as_default():
			with self.session.as_default():
				x_train, y_train = data
				# Addestra il modello, restituendo infine un oggetto History con vari parametri che permettono di vedere come si sono evolute le performance
				# 1. numpy array o lista di numpy array (secondo la dimensionalità attesa)
				# 2. come sopra
				# 3. numero di sample da utilizzare prima di aggiornare i pesi
				# 4. numero di iterazioni da fare sui dati in input
				# 5. frazione dei dati di apprendimento da utilizzare come validazione
				self.model.fit(x_train, y_train, batch_size=3, epochs=5, verbose=1)


	def test(self, data):
		with self.graph.as_default():
			with self.session.as_default():
				x_test, y_test = data

				return self.model.evaluate(x_test, y_test, verbose=1)
		

	def predict(self,data):
		with self.graph.as_default():
			with self.session.as_default():
				return self.model.predict(data)


	def get_weights(self):
		with self.graph.as_default():
			with self.session.as_default():	
				return self.model.get_weights()


	def set_weights(self, weights):	
		with self.graph.as_default():
			with self.session.as_default():	
				return self.model.set_weights(weights)


	def export(self):
		with self.graph.as_default():
			with self.session.as_default():	
				file_name = 'my_model' + str(datetime.timestamp(datetime.now())) + '.h5'
				file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), file_name)
				file = open(file_path, 'wb+')
				self.model.save(file_path)
				file.close()
				return open(file_path, 'rb'), file_path