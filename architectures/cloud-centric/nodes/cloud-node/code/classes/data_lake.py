import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import numpy as np
from keras.utils import np_utils
from io import StringIO


class DataLake:
	      

	def __init__(self):
		self.mean = []
		self.std = []
		self.first = False # per correggere apply in cui la colonna 0 viene letta due volte (da capire perche')
		self.fileDir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'data')

		# Crea un DataFrame da un documento formattato come un csv
		label = pd.read_csv(os.path.join(fileDir, 'profile.txt'), sep='\t', header=None)

		# Seleziona la prima colonna con label[0] (Cooler Condition) ovvero il parametro che vogliamo predire
		# Codifica ogni valore dell'array passato in un numero, restituendo l'array creato in questo modo ([0]) e i valori unici incontrati ([1])
		# Converte ogni intero nell'array passato in una codifica one-hot (1 -> 001, 2 -> 010, 3 -> 100), necessaria per la categorical_crossentropy
		# Ricordiamo che in questo caso creiamo l'associazione 1 <-> 100, 20 <-> 010, 100 <-> 001
		label = np_utils.to_categorical(label[0].factorize()[0])
		self.label = label

		data = [os.path.join(fileDir, 'TS1.txt'),os.path.join(fileDir, 'TS2.txt'),os.path.join(fileDir, 'TS3.txt'),os.path.join(fileDir, 'TS4.txt')]
		df = pd.DataFrame()
		for txt in data:
			read_df = pd.read_csv(txt, sep='\t', header=None)
			df = df.append(read_df)

		df = df.apply(self.__train_scale)

		# sort_index(): ordina ogni colonna del DataFrame in senso crescente
		# values: restituisce i valori del DataFrame (senza divisione in colonne e righe)
		# reshape: rimodella il DataFrame creando un ndarray 3D con gli stessi dati ma dividendo i dati in 4 colonne e ogni dato un array da 60 elementi
		# 	(-1 indica che non abbiamo preferenze per le righe, quindi saranno calcolate direttamente come risultato della divisione dei dati)
		# transpose: ogni numero indica un asse, ed essendo in un array 3D abbiamo 3 assi (indicati con 0, 1 e 2)
		# 	in base alla posizione in cui si passa questi numeri, la loro posizione viene scambiata, quindi nel nostro caso otteniamo righe con 60 colonne da 4 elementi l'uno
		# In definitiva, otteniamo un array 3D in cui:
		#	df[0] = ci permette di accedere un array 2D in cui abbiamo la misurazione completa effettuata nel ciclo 0 dai 4 sensori (ciclo = 60 secondi)
		#	df[0][0] = ci permette di accedere un array 1D in cui abbiamo la misurazione effettuata dai 4 sensori nel secondo 0 del ciclo 0
		#	df[0][0][0] = ci permette di accedere al valore letto dal sensore 0 nel secondo 0 del ciclo 0
		df = df.sort_index(kind='mergesort').values.reshape(-1,4,60).transpose(0,2,1)

		self.df = df


	def get_training_data(self):
		# Divide ogni lista o array fornita in ingresso in due set (training e test) in base al parametro di test_size
		return train_test_split(self.df, self.label, test_size=0.2)


	def add_data(self, data, outcome):
		for name in ['TS1', 'TS2', 'TS3', 'TS4']:
			filePath = os.path.join(self.fileDir, name + '.txt')
			f = open(filePath, "a")
			f.write(data[name])
			f.close()
		filePath = os.path.join(self.fileDir, 'profile.txt')
		f = open(filePath, "a")
		f.write(outcome)
		f.close()


	def transform(self, data):
		df = pd.DataFrame()

		for txt in data:
			read_df = pd.read_csv(StringIO(txt), sep='\t', header=None)
			df = df.append(read_df)

		df = df.apply(self.__predict_scale)

		df = df.sort_index(kind='mergesort').values.reshape(-1,4,60).transpose(0,2,1)
		
		return df


	def __train_scale(self,df):
		# Ad ogni dato di ogni colonna, sottrae la media e divide per la deviazione standard (entrambi calcolati sulla colonna considerata)
		# In definitiva, standardizziamo la variabile aleatoria distribuita seconda una certa media e varianza ad una variabile con distribuzione standard
		# quindi con media zero e varianza 1
		if self.first == False: 
			self.first = True
		else:
			self.mean.append(df.mean(axis = 0))
			self.std.append(df.std(axis = 0))
		return (df - df.mean(axis=0)) / df.std(axis=0)


	def __predict_scale(self,df):
		# Ad ogni dato di ogni colonna, sottrae la media e divide per la deviazione standard (entrambi calcolati sulla colonna considerata)
		# In definitiva, standardizziamo la variabile aleatoria distribuita seconda una certa media e varianza ad una variabile con distribuzione standard
		# quindi con media zero e varianza 1
		return (df - self.mean[df.name]) / self.std[df.name]