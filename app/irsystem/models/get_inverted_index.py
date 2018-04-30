import csv
import os
import json
import numpy as np
import re
import math

mydict = {}
with open("inverted_index.csv", 'rb') as f:
	mycsv = csv.reader(f, delimiter = ",")
	for x, row in enumerate(mycsv):
		if x!=0:
			mydict[row[0]] = np.fromstring(row[1])