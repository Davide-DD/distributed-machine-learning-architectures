import os
import sys
import random
import shutil



def count_lines(file_path):
	with open(file_path) as f:
		lines_number = sum(1 for line in f)
		f.close()
	return lines_number


def read_specific_lines(file_name, numbers):
    file = open(file_name, "r")
    result = ""
    for i, line in enumerate(file):
        if i in numbers:
            result += line
    file.close()
    return result


def get_lines(lines_number, selected_lines, max_line_number=None):
	state = 0
	result = []
	for i in range(0, lines_number):
		rand_int = random.randrange(0, 732) + state * 732
		while rand_int in selected_lines or rand_int in result:
			rand_int = random.randrange(0, 732) + state * 732
		state += 1
		if state == 3:
			state = 0
		result.append(rand_int)
	return result


def create_node_instance(destination_path, node_type_path, instance_number, train_files, test_files):
	node_instance_path = os.path.join(destination_path, os.path.basename(node_type_path) + '-' + str(instance_number))
	shutil.copytree(node_type_path, node_instance_path)

	train_path = os.path.join(os.path.join(node_instance_path, 'code'), 'data')
	os.mkdir(train_path)

	test_path = os.path.join(os.path.join(node_instance_path, 'code'), 'test')
	os.mkdir(test_path)

	for name, text in train_files.items():
		file_path = os.path.join(train_path, name)
		with open(file_path, 'w+') as f:
			f.write(text)
			f.close()

	for name, text in test_files.items():
		file_path = os.path.join(test_path, name)
		with open(file_path, 'w+') as f:
			f.write(text)
			f.close()


def get_examples(examples_number, selected_lines):
	result_files = {}
	result_lines = get_lines(examples_number, selected_lines)
	for file in os.listdir(dataset_path):
		file_path = os.path.join(dataset_path, file)
		if '.DS_Store' not in file:
			result_files[file] = read_specific_lines(file_path, result_lines)
	return result_files, result_lines


def get_node_types():
	result = []

	for folder in os.listdir(architecture_path):
		folder_path = os.path.join(architecture_path, folder)
		if os.path.isdir(folder_path):
			result.append(folder_path)

	return result



if len(sys.argv) < 3:
	print('[Usage] {} <test_architecture_name> <dataset_path>'.format(sys.argv[0]))
	exit(0)

script_dir = os.path.dirname(os.path.abspath(__file__))
test_architecture_path = os.path.join(script_dir, sys.argv[1])
architecture_path = os.path.join(os.path.dirname(script_dir), 'nodes')
dataset_path = sys.argv[2]

try:
	os.mkdir(test_architecture_path)
except Exception as e:
	shutil.rmtree(test_architecture_path)

selected_lines = []
for nt in get_node_types():
	nt_basename = os.path.basename(nt)
	nodes_number = int(input('Node type found: ' + nt_basename + '. How many nodes of this type you want to instantiate?\n'))
	examples_number = int(input('How many records do you want to give to each node\'s dataset?\n'))
	destination_path = os.path.join(test_architecture_path, nt_basename)
	os.mkdir(destination_path)
	if nt_basename == 'fog-node':
		test_files, test_lines = get_examples(100, selected_lines)
		selected_lines += test_lines
		for i in range(0, nodes_number):
			train_files, train_lines = get_examples(examples_number, selected_lines)
			create_node_instance(destination_path, nt, i, train_files, test_files)
			selected_lines += train_lines