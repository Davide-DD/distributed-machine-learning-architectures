import pandas as pd
import os
import numpy as np
from keras.utils import np_utils
from io import StringIO


class DataLake:
	      

	def __init__(self):
		self.mean = []
		self.std = []
		self.first = True

		dirname = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
		train_dir = os.path.join(dirname, 'data')
		test_dir = os.path.join(dirname, 'test')

		self.train_df, self.train_label = self.transform(([os.path.join(train_dir, 'TS1.txt'), os.path.join(train_dir, 'TS2.txt'), 
			os.path.join(train_dir, 'TS3.txt'), os.path.join(train_dir, 'TS4.txt')], os.path.join(train_dir, 'profile.txt')))

		self.test_df, self.test_label = self.transform(([os.path.join(test_dir, 'TS1.txt'), os.path.join(test_dir, 'TS2.txt'), 
			os.path.join(test_dir, 'TS3.txt'), os.path.join(test_dir, 'TS4.txt')], os.path.join(test_dir, 'profile.txt')))


	def transform(self, data):
		scale_fun = self.__predict_scale

		examples = data

		if type(data) is tuple:
			examples, classes = data

			scale_fun = self.__train_scale

			if os.path.isfile(classes):
				label = pd.read_csv(classes, sep='\t', header=None)
			else:
				label = pd.read_csv(StringIO(classes), sep='\t', header=None)

			# Seleziona la prima colonna con label[0] (Cooler Condition) ovvero il parametro che vogliamo predire
			# Codifica ogni valore dell'array passato in un numero, restituendo l'array creato in questo modo ([0]) e i valori unici incontrati ([1])
			# Converte ogni intero nell'array passato in una codifica one-hot (1 -> 001, 2 -> 010, 3 -> 100), necessaria per la categorical_crossentropy
			# Ricordiamo che in questo caso creiamo l'associazione 1 <-> 100, 20 <-> 010, 100 <-> 001
			label = np_utils.to_categorical(label[0].factorize()[0])

		df = pd.DataFrame()
			
		for txt in examples:
			if os.path.isfile(txt):
				read_df = pd.read_csv(txt, sep='\t', header=None)
			else:
				read_df = pd.read_csv(StringIO(txt), sep='\t', header=None)
			df = df.append(read_df)

		df = df.apply(scale_fun)

		df = df.sort_index(kind='mergesort').values.reshape(-1,4,60).transpose(0,2,1)
		
		return df, label


	def get_training_data(self):
		return self.train_df, self.train_label


	def get_test_data(self):
		return self.test_df, self.test_label


	def __train_scale(self,df):
		# Ad ogni dato di ogni colonna, sottrae la media e divide per la deviazione standard (entrambi calcolati sulla colonna considerata)
		# In definitiva, standardizziamo la variabile aleatoria distribuita seconda una certa media e varianza ad una variabile con distribuzione standard
		# quindi con media zero e varianza 1
		if self.first: 
			self.first = False
		else:
			self.mean.append(df.mean(axis = 0))
			self.std.append(df.std(axis = 0))
		return (df - df.mean(axis=0)) / df.std(axis=0)


	def __predict_scale(self,df):
		# Ad ogni dato di ogni colonna, sottrae la media e divide per la deviazione standard (entrambi calcolati sulla colonna considerata)
		# In definitiva, standardizziamo la variabile aleatoria distribuita seconda una certa media e varianza ad una variabile con distribuzione standard
		# quindi con media zero e varianza 1
		return (df - self.mean[df.name]) / self.std[df.name]