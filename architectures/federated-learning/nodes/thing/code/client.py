import numpy as np
import requests
import json
import time
import os
import sys


if len(sys.argv) < 2:
	print('[Usage] {} <edge ip:port>'.format(sys.argv[0]))
	exit(0)

predict_address = sys.argv[1]

dirPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
ts1_f = open(os.path.join(dirPath, 'TS1.txt'), 'r')
ts2_f = open(os.path.join(dirPath, 'TS2.txt'), 'r')
ts3_f = open(os.path.join(dirPath, 'TS3.txt'), 'r')
ts4_f = open(os.path.join(dirPath, 'TS4.txt'), 'r')
profile_f = open(os.path.join(dirPath, 'profile.txt'), 'r')

for profile in profile_f:
	ts1 = ts1_f.readline()
	ts2 = ts2_f.readline()
	ts3 = ts3_f.readline()
	ts4 = ts4_f.readline()
	data = {
		'TS1': ts1,
		'TS2': ts2,
		'TS3': ts3,
		'TS4': ts4,
		'outcome': profile
	}
	url = 'http://' + predict_address + "/predict"
	content = str(requests.post(url, json=data).content)
	if '3' in content:
		print('close to total failure')
	elif '20' in content:
		print('reduced efficiency')
	elif '100' in content:
		print('full efficiency')
	else: print('model is not ready')