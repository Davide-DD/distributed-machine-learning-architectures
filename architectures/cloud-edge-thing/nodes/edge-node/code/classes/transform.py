import pandas as pd
import numpy as np
from io import StringIO


class Transform:

	def __init__(self):
		self.mean = None
		self.std = None


	def load(self,mean,std):
		self.mean = mean
		self.std = std


	def transform(self,data):
		df = pd.DataFrame()

		for txt in data:
			read_df = pd.read_csv(StringIO(txt), sep='\t', header=None)
			df = df.append(read_df)

		df = df.apply(self.__scale)

		df = df.sort_index(kind='mergesort').values.reshape(-1,4,60).transpose(0,2,1)
		
		return df


	def __scale(self,df):
		return (df - self.mean[df.name]) / self.std[df.name]
