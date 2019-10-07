import os


class Logger:

	def __init__(self):
		single_tests_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'log_single_tests.txt')
		voted_tests_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'log_voted_tests.txt')
		loaded_peers_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'log_loaded_peers.txt')
		selected_peers_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'log_selected_peers.txt')

		try:
			os.remove(single_tests_path)
			os.remove(voted_tests_path)
			os.remove(loaded_peers_path)
			os.remove(selected_peers_path)
		except Exception as e:
			print(e)

		self.single_tests_file = open(single_tests_path, 'a+')
		self.voted_tests_file = open(voted_tests_path, 'a+')
		self.selected_peers_file = open(selected_peers_path, 'a+')
		self.loaded_peers_file = open(loaded_peers_path, 'a+')


	def log_single_test(self,results):
		self.single_tests_file.write(str(results[0][1]))
		for r in results[1:]:
			self.single_tests_file.write('\t' + str(r[1]))
		for i in range(0, 10 - len(results)):
			self.single_tests_file.write('\t' + 'NaN')
		self.single_tests_file.write('\n')
		self.single_tests_file.flush()


	def log_voted_test(self,result):
		self.voted_tests_file.write(result + '\n')
		self.voted_tests_file.flush()


	def log_loaded_peers(self,results):
		self.loaded_peers_file.write(str(results[0].address))
		for r in results[1:]:
			self.loaded_peers_file.write('\t' + str(r.address))
		self.loaded_peers_file.write('\n')
		self.loaded_peers_file.flush()


	def log_selected_peers(self,results):
		self.selected_peers_file.write(str(results[0].address))
		for r in results[1:]:
			self.selected_peers_file.write('\t' + str(r.address))
		self.selected_peers_file.write('\n')
		self.selected_peers_file.flush()