#!/bin/bash

for pid in $(ps -A | grep 'server.py' | awk '{print $1}')
do
	echo $pid
	kill -2 $pid
done
