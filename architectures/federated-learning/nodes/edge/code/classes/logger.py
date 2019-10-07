import os


class Logger:

	def __init__(self):
		tests_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'log_tests.txt')
		
		try:
			os.remove(tests_path)
		except Exception as e:
			print(e)

		self.tests_file = open(tests_path, 'w+')
		

	def log_test(self,result):
		self.tests_file.write(str(result) + '\n')
		self.tests_file.flush()