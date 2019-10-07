import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import sys


plt.rcParams['figure.figsize'] = (19.2, 8.7)
index = 0

def show_accuracy(df):
	global index
	
	df.plot(kind='line')
	plt.xlabel('iterations')
	plt.ylabel('accuracy')
	plt.savefig(str(index) + '.png', bbox_inches='tight')

	print('Minima: ' + str(df.min(axis=1).min() * 100) + ' %', file=report)
	print('Primo indice della minima: ' + str(df.min(axis=1).idxmin()), file=report)
	print('Massima: ' + str(df.max(axis=1).max() * 100) + ' %', file=report)
	print('Primo indice della massima: ' + str(df.max(axis=1).idxmax()) + '\n', file=report)
	print('Finale: ' + str(df[0].iloc[-1]), file=report)

	index += 1

def calculate_node_info(logs):
	accuracy_df = pd.read_csv(logs['log_tests.txt'], sep='\t', header=None)
	show_accuracy(accuracy_df)

arch_path = sys.argv[1]
logs = {}
for nt in os.listdir(arch_path):
	if os.path.isdir(os.path.join(arch_path, nt)):
		nt_path = os.path.join(arch_path, nt)
		for ni in os.listdir(nt_path):
			if os.path.isdir(os.path.join(nt_path, ni)):
				ni_path = os.path.join(os.path.join(nt_path, ni), 'code')
				result = {}
				for log in os.listdir(ni_path):
					log_path = os.path.join(ni_path, log)
					if os.path.isfile(log_path) and 'log' in log:
						result[log] = log_path
				logs[ni] = result

report = open('report.txt', 'w')
print('\n------------------- ACCURATEZZA -------------------', file=report)
calculate_node_info(logs['edge-0'])
print('')