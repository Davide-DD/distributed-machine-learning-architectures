import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import sys


plt.rcParams['figure.figsize'] = (19.2, 8.7)
index = 0

def show_selected_peers(df):
	global index

	unique_peers_contacted = df[0].nunique()
	print('Numero di peer unici contattati: ' + str(unique_peers_contacted), file=report)

	# Peer più frequentemente contattati
	df[0].value_counts().plot(kind='bar')
	plt.xlabel('peers')
	plt.ylabel('appearances')
	plt.savefig(str(index) + '.png', bbox_inches='tight')
	index += 1

	# Peer più frequentemente inviati agli altri peer
	df = df.drop(columns=0).apply(pd.Series.value_counts).sum(axis=1)
	unique_peers_suggested = df.shape[0]
	print('Numero di peer unici suggeriti: ' + str(unique_peers_suggested), file=report)
	df.plot(kind='bar')
	plt.xlabel('peers')
	plt.ylabel('appearances')
	plt.savefig(str(index) + '.png', bbox_inches='tight')
	index += 1

	return unique_peers_contacted, unique_peers_suggested

def show_loaded_peers(df):
	global index

	# Peer più frequentemente caricati dagli altri peer
	df = df.apply(pd.Series.value_counts).sum(axis=1)
	unique_peers_loaded = df.shape[0]
	print('Numero di peer unici conosciuti: ' + str(unique_peers_loaded), file=report)
	df.plot(kind='bar')
	plt.xlabel('peers')
	plt.ylabel('appearances')
	plt.savefig(str(index) + '.png', bbox_inches='tight')
	index += 1

	return unique_peers_loaded

def calculate_single_accuracy(df,ax):
	df[0].plot(kind='line',ax=ax,label='Single model', legend=True)

	print('ACCURATEZZA SINGOLARE', file=report)
	print('Minima: ' + str(df.min(axis=1).min() * 100) + ' %', file=report)
	print('Primo indice della minima: ' + str(df.min(axis=1).idxmin()), file=report)
	print('Massima: ' + str(df.max(axis=1).max() * 100) + ' %', file=report)
	print('Primo indice della massima: ' + str(df.max(axis=1).idxmax()) + '\n', file=report)

	return df.max(axis=1).idxmax()


def calculate_ensemble_accuracy(df,ax):	
	df = df.rename(columns={0:'Model cache'})
	df.plot(kind='line',ax=ax)

	print('ACCURATEZZA COLLETTIVA', file=report)
	print('Minima: ' + str(df.min(axis=1).min() * 100) + ' %', file=report)
	print('Primo indice della minima: ' + str(df.min(axis=1).idxmin()), file=report)
	print('Massima: ' + str(df.max(axis=1).max() * 100) + ' %', file=report)
	print('Primo indice della massima: ' + str(df.max(axis=1).idxmax()) + '\n', file=report)

	return df['Model cache'].iloc[-1]


def show_compared_accuracy(single_df, voted_df):
	global index
	figure = plt.figure()
	ax = figure.gca()
	ax.set(xlabel="iterations", ylabel="accuracy")
	best_single_accuracy_index = calculate_single_accuracy(single_df,ax)
	last_ensemble_accuracy = calculate_ensemble_accuracy(voted_df,ax)
	figure.savefig(str(index) + '.png', bbox_inches='tight')
	index += 1
	plt.close()
	return best_single_accuracy_index, last_ensemble_accuracy


def calculate_overall_accuracy(bsai, lea):
	print('ACCURATEZZA FINALE', file=report)
	print(str(lea * 100) + ' %', file=report)

	print('NUMERO DI ITERAZIONI NECESSARIE AL RAGGIUNGIMENTO DELL\'ACCURATEZZA MASSIMA', file=report)
	print(str(bsai), file=report)


def calculate_node_info(logs):
	voted_accuracy_df = pd.read_csv(logs['log_voted_tests.txt'], sep='\t', header=None)
	single_accuracy_df = pd.read_csv(logs['log_single_tests.txt'], sep='\t', header=None)
	selected_peers_df = pd.read_csv(logs['log_selected_peers.txt'], sep='\t', header=None)
	loaded_peers_df = pd.read_csv(logs['log_loaded_peers.txt'], sep='\t', header=None)

	print('PEER DISCOVERY', file=report)
	unique_peers_contacted, unique_peers_suggested = show_selected_peers(selected_peers_df)
	unique_peers_loaded = show_loaded_peers(loaded_peers_df)
	print(file=report)

	best_single_accuracy_index, last_ensemble_accuracy = show_compared_accuracy(single_accuracy_df, voted_accuracy_df)

	calculate_overall_accuracy(best_single_accuracy_index, last_ensemble_accuracy)

	return unique_peers_contacted, unique_peers_suggested, unique_peers_loaded, best_single_accuracy_index, last_ensemble_accuracy 


def calculate_global_info(upc_arr, ups_arr, upl_arr, bsai_arr, lea_arr):
	print('\n------------------- STATISTICHE COMPLESSIVE -------------------', file=report)

	mean_peers_contacted = sum(upc_arr) / len(upc_arr)
	mean_peers_suggested = sum(ups_arr) / len(ups_arr)
	mean_peers_loaded = sum(upl_arr) / len(upl_arr)

	print('NUMERO MEDIO DI PEER UNICI CONTATTATI PER NODO: ' + str(mean_peers_contacted), file=report)
	print('NUMERO MEDIO DI PEER UNICI SUGGERITI PER NODO: ' + str(mean_peers_suggested), file=report)
	print('NUMERO MEDIO DI PEER UNICI CONOSCIUTI PER NODO: ' + str(mean_peers_loaded), file=report)

	mean_best_index = sum(bsai_arr) / len(bsai_arr)
	mean_final_acc = sum(lea_arr) / len(lea_arr)

	print('INDICE MEDIO DI RAGGIUNGIMENTO DELL\'ACCURATEZZA MASSIMA', file=report)
	print(mean_best_index, file=report)
	print('\nACCURATEZZA FINALE MEDIA', file=report)
	print(str(mean_final_acc * 100) + ' %', file=report)


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
upc_arr = []
ups_arr = []
upl_arr = []
bsai_arr = []
lea_arr = []
for nn, nl in logs.items():
	print('\n------------------- ' + nn + ' -------------------', file=report)
	upc, ups, upl, bsai, lea = calculate_node_info(nl)
	upc_arr.append(upc)
	ups_arr.append(ups)
	upl_arr.append(upl)
	bsai_arr.append(bsai)
	lea_arr.append(lea)
calculate_global_info(upc_arr, ups_arr, upl_arr, bsai_arr, lea_arr)
print('')