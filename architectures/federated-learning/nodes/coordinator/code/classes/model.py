from keras.models import *
from keras.layers import *
import numpy as np
import tensorflow as tf
import os



class Model:


	def __init__(self):
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
		self.graph = tf.get_default_graph()


	def update(self,delta):
		with self.graph.as_default():
			weights = self.model.get_weights()
			for i in range(0, len(weights)):
				weights[i] = np.add(weights[i], np.asarray(delta[i]))
			self.model.set_weights(weights)


	def predict(self,data):
		with self.graph.as_default():
			predictions = self.model.predict(data)
			result = np.where(predictions[0] == np.amax(predictions[0]))
			if result[0][0] == 0:
				return '3'
			elif result[0][0] == 1:
				return '20'
			else:
				return '100'


	def export(self):
		with self.graph.as_default():
			file_name = 'my_model.h5'
			file_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), file_name)
			self.model.save(file_path)  # creates a HDF5 file 'my_model.h5'
			return open(file_path, 'rb')