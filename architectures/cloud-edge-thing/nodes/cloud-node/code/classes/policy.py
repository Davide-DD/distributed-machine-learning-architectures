class Policy:


	def __init__(self):
		self.wrong_predictions = 0


	def update_status(self):
		self.wrong_predictions += 1


	def is_respected(self):
		if self.wrong_predictions < 25:
			return True
		self.wrong_predictions = 0
		return False