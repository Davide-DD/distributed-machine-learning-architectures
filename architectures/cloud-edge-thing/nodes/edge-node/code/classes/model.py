from keras.models import *
from keras.layers import *
from keras.backend import clear_session
from numpy import where,amax
import tensorflow as tf



class Model:


	def __init__(self):
		self.model = None
		self.graph = None


	def load(self,exported_model):
		del self.model
		del self.graph
		clear_session()
		self.model = load_model(exported_model)
		self.graph = tf.get_default_graph()
		

	def predict(self,data):
		if self.model != None:
			with self.graph.as_default():
				predictions = self.model.predict(data)
				result = where(predictions[0] == amax(predictions[0]))
				if result[0][0] == 0:
					return '3'
				elif result[0][0] == 1:
					return '20'
				else:
					return '100'
		else:
			return 'Model not ready'