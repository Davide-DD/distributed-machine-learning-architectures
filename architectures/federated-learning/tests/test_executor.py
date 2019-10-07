import sys
import os
import random
import socket


if len(sys.argv) < 2:
	print('[Usage] {} <test_architecture_name>'.format(sys.argv[0]))
	exit(0)

host_address = socket.gethostbyname(socket.gethostname())
test_architecture_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), sys.argv[1])
base_port = '5'
edge_addresses = []

node_types = {}
for nt in os.listdir(test_architecture_path):
	temp_path = os.path.join(test_architecture_path, nt)
	if os.path.isdir(temp_path):
		node_types[nt] = temp_path

index = 0
edge_addresses = []
for ni in os.listdir(node_types['edge']):
	temp_path = os.path.join(node_types['edge'], ni)
	if os.path.isdir(temp_path):
		ni_path = os.path.join(os.path.join(temp_path, 'code'), 'server.py')
		if index < 10:
			port = base_port + '00' + str(index)
		else:
			port = base_port + '0' + str(index)
		address = host_address + ':' + port
		edge_addresses.append(address)
		os.system('python3 ' + ni_path + ' ' + port + ' &')
		print('Edge ' + str(port) + ' started')
		index += 1

coordinator_port = base_port + '100'
for ni in os.listdir(node_types['coordinator']):
	temp_path = os.path.join(node_types['coordinator'], ni)
	if os.path.isdir(temp_path):
		ni_path = os.path.join(os.path.join(os.path.join(node_types['coordinator'], ni), 'code'), 'server.py')
		command = 'python3 ' + ni_path + ' ' + coordinator_port
		for address in edge_addresses:
			command += ' ' + address
		os.system(command + ' &')
		print('Coordinator started')

aggregators_number = 0
for ni in os.listdir(node_types['aggregator']):
	temp_path = os.path.join(node_types['aggregator'], ni)
	if os.path.isdir(temp_path):
		aggregators_number += 1

for ni in os.listdir(node_types['master-aggregator']):
	temp_path = os.path.join(node_types['master-aggregator'], ni)
	if os.path.isdir(temp_path):
		ni_path = os.path.join(os.path.join(os.path.join(node_types['master-aggregator'], ni), 'code'), 'server.py')
		command = 'python3 ' + ni_path + ' ' + str(aggregators_number) + ' ' + host_address + ':' + coordinator_port + ' ' + base_port + '200'
		os.system(command + ' &')
		print('Master aggregator started')

edges_numbers = len(edge_addresses) // aggregators_number
index = 0
aggregator_address = []
for ni in os.listdir(node_types['aggregator']):
	temp_path = os.path.join(node_types['aggregator'], ni)
	if os.path.isdir(temp_path):
		ni_path = os.path.join(os.path.join(os.path.join(node_types['aggregator'], ni), 'code'), 'server.py')
		if index < 10:
			port = base_port + '30' + str(index)
		else:
			port = base_port + '3' + str(index)
		command = 'python3 ' + ni_path + ' ' + str(edges_numbers) + ' ' + host_address + ':' + base_port + '200 ' + port
		os.system(command + ' &')
		print('Aggregator ' + port + ' started')
		index += 1

print('Test running...')
