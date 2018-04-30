import csv
import os
import json
import numpy as np
import re
import math

mydict = {}
with open("goodwords.csv", 'rb') as f:
	mycsv = csv.reader(f, delimiter = ",")
	for x, row in enumerate(mycsv):
		if x!=0:
			mydict[row[0]] = [row[1], row[2], row[3]]

def	get_avglikes(tag):
	return mydict[tag][0]

def	get_likescore(tag):
	val = float(mydict[tag][1])
	if val > 1:
		return float(val-1)*1.0
	elif val < 1:
		return val*-1
	elif val == 1:
		return 0

def	get_totalposts(tag):
	return mydict[tag][2]

print(get_likescore("dog"))
