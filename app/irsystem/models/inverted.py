import json
import numpy as np
import re
import os
import math
import enchant
import csv
from parsers_and_TFidf_setup import *


def serve_jsons():
    path_to_json_dir = os.getcwd()+'/../../../app/static/json/'
    for _, _, filenames in os.walk(path_to_json_dir):
        json_files = [ f for f in filenames if f.endswith("json") ]
    return json_files

word_to_int_dict, tag_to_int_dict, int_to_word_dict, int_to_tag_dict, \
    word_TDF, tag_TDF, word_inv_idx, tag_inv_idx, post_dict, word_TF_IDF, doc_norms, idf_dict = process_list_of_jsons(serve_jsons())

with open('inverted_index.csv', 'w') as csvfile:
    fieldnames = ['word', 'numpyarray']
    writer = csv.writer(csvfile, dialect='excel')


    tag_num = -1
    for k in tag_inv_idx.keys():
        tag_num += 1
        if tag_num%500==0:print (tag_num)
        lst = [k]
        i = -1
        for e in tag_inv_idx[k]:
            i+=1
            if e !=0 :
                lst.append((i,e))
            
        writer.writerow(lst)