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


	def train(self,data):

		X_train, X_test, y_train, y_test = data

		# Addestra il modello, restituendo infine un oggetto History con vari parametri che permettono di vedere come si sono evolute le performance
		# 1. numpy array o lista di numpy array (secondo la dimensionalità attesa)
		# 2. come sopra
		# 3. numero di sample da utilizzare prima di aggiornare i pesi
		# 4. numero di iterazioni da fare sui dati in input
		# 5. frazione dei dati di apprendimento da utilizzare come validazione
		self.model.fit(X_train, y_train, batch_size=32, epochs=10, validation_split=0.2, verbose=1, shuffle=True)

		print(self.model.evaluate(X_test, y_test, verbose=1))


	def export(self):
		fileName = 'my_model.h5'
		filePath = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), fileName)
		self.model.save(fileName)  # creates a HDF5 file 'my_model.h5'
		return open(filePath, 'rb')