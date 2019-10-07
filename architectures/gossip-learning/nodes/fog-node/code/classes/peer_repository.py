from classes.aged_peer import AgedPeer
import random
import math


class PeerRepository:


def __init__(self, max_size, healing_factor, swap_factor, my_info, peers_info, logger):
	self.max_size = max_size # Dimensione massima della lista di peer
	self.separation_factor = math.ceil(self.max_size / 2) - 1 # Numero di separazione per garantire la dimensione massima
	self.healing_factor = healing_factor # Numero di peer da ignorare in base alla loro età
	self.swap_factor = swap_factor # Fattore di modifica della lista di peer per assicurare che 2 liste che vengono unite
	# non diventino troppo simili, dato che potrebbe inficiare la capacità di ritrovamento di nuovi nodi

	self.my_info = AgedPeer(my_info)
	self.aged_peers = []
	for p in peers_info:
		self.aged_peers.append(AgedPeer(p))

	self.logger = logger


	def select(self):
		if not self.aged_peers:
			return []

		result = []

		self.aged_peers.sort(key=lambda x: x.age)

		if self.healing_factor == 0:
			newest_peers = list(self.aged_peers)
			oldest_peers = []
		else:
			oldest_peers = self.aged_peers[-self.healing_factor:]
			newest_peers = list(self.aged_peers[:-self.healing_factor])

		random.shuffle(newest_peers)
		temp_peers = newest_peers + oldest_peers

		result = temp_peers[:self.separation_factor]
		result.append(self.my_info)

		self.__increase_age()

		result.sort(key=lambda x: x.age)

		self.logger.log_selected_peers([result[-1]] + result[:-1])

		return result[-1], result[:-1]


def load(self, aged_peers):
	# Aggiunge i peer ricevuti a quelli mantenuti in locale
	for p in aged_peers:
		self.aged_peers.append(p)

	# Rimuove i duplicati mantenendo il piu' giovane
	temp = []
	for i in self.aged_peers:
		if i not in temp:
			temp.append(i)
		else:
			for j in temp:
				if i == j:
					if i.age < j.age:
						temp.remove(j)
						temp.append(i)

	# Riordina in base all'età
	temp.sort(key=lambda x: x.age)

	if len(temp) > self.max_size:

		# INIZIO ELIMINAZIONE PEER
		if self.healing_factor > 0:
			
			# Rimuove alcuni peer più vecchi: più alto l'healing factor, più aggressivo l'algoritmo sarà a rimuovere potenziali link down
			temp = temp[:-min(self.healing_factor, len(temp) - self.max_size)]
		
		# Rimuove alcuni peer più giovani: più è basso e più le liste di peer tra questo peer e quello da cui è stata ricevuta la lista
		# diventeranno simili, portando a una riduzione della possibilità di scoprire nuovi peer ricontattando quest'ultimo 
		temp = temp[min(self.swap_factor, len(temp) - self.max_size):]

		# Rimuove peer a caso per ridurre la lista fino a max_size elementi
		random_delete_number = len(temp) - self.max_size
		for i in range(0, random_delete_number):
			temp.pop(random.randrange(len(temp)))

		# FINE ELIMINAZIONE PEER


	# Salva il risultato delle modifiche fatte finora
	self.aged_peers = temp

	self.__increase_age()

	self.logger.log_loaded_peers(self.aged_peers)


	def __increase_age(self):
		for peer in self.aged_peers:
			peer.age = peer.age + 1