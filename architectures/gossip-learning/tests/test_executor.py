import sys
import os
import random
import socket


if len(sys.argv) < 3:
	print('[Usage] {} <test_architecture_name> <peers_per_node>'.format(sys.argv[0]))
	exit(0)

test_architecture_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), sys.argv[1])
peers_per_node = int(sys.argv[2])
host_address = socket.gethostbyname(socket.gethostname())

peer_addresses = []
for nt in os.listdir(test_architecture_path):
	nt_path = os.path.join(test_architecture_path, nt)

	if nt == 'fog-node':
		nodes_number = len([name for name in os.listdir(nt_path)])
		for i in range(0, nodes_number):
			if i < 10:
				peer_addresses.append(host_address + ':500' + str(i))
			else:
				peer_addresses.append(host_address + ':50' + str(i))

		index = 0

		for ni in os.listdir(nt_path):
			peers_subset = []
			for i in range(0, peers_per_node):
				peer_index = random.randint(0, len(peer_addresses) - 1)
				while peer_addresses[peer_index] in peers_subset:
					peer_index = random.randint(0, len(peer_addresses) - 1)
				peers_subset.append(peer_addresses[peer_index])

			server_path = os.path.join(os.path.join(os.path.join(nt_path, ni), 'code'), 'server.py')
			command = 'python3 ' + server_path + ' '
			if index < 10:
				command += '500' + str(index)
			else:
				command += '50' + str(index)
			for address in peers_subset:
				command += ' ' + str(address)
			index += 1
			os.system(command + ' &')

print('Test running...')