class AgedPeer:


	def __init__(self, address, age=0):
		self.address = address
		self.age = age


	def __eq__(self, other):
		if isinstance(other, AgedPeer):
			return self.address == other.address
		return False

	@staticmethod
	def from_json(json_object):
		return AgedPeer(json_object['address'], json_object['age'])