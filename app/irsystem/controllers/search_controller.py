from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.cosinesim import input_to_tags
from app.irsystem.models.parsers_and_TFidf_setup import process_list_of_jsons
from numpy import linalg as LA
from scipy.sparse.linalg import svds
import os
import ast
import csv

# def serve_jsons():
#     path_to_json_dir = os.getcwd()+'/app/static/json/'
#     for _, _, filenames in os.walk(path_to_json_dir):
#         json_files = [ f for f in filenames if f.endswith("json") ]
#         return json_files

# profile_lst = serve_jsons()
# word_to_int_dict, tag_to_int_dict, int_to_word_dict, int_to_tag_dict, \
# word_TDF, tag_TDF, word_inv_idx, tag_inv_idx, post_dict, word_TF_IDF, doc_norms, idf_dict = process_list_of_jsons(profile_lst)

word_to_int_dict = {}
with open(os.getcwd()+"/app/irsystem/models/word_to_int.csv", 'rb') as f:
    mycsv = csv.reader(f, delimiter = ",")
    for x, row in enumerate(mycsv):
        if x!=0:
            word_to_int_dict[row[0]] = int(row[1])

post_dict = {}
with open(os.getcwd()+"/app/irsystem/models/post_dict.csv", 'rb') as f:
    mycsv = csv.reader(f, delimiter = ",")
    for x, row in enumerate(mycsv):
        if x!=0:
            post_dict[row[0]] = (row[1])

# numWords = len(word_to_int_dict)
# inverted_index = {}
# with open("/../models/inverted_index.csv", 'r') as f:
#     mycsv = csv.reader(f, delimiter = ",")
#     for x, row in enumerate(mycsv):
#         #if x==0: print (row)
#         #if x%1000==0: print (x)
#         arr = np.zeros(numWords)
#         for enum, e in enumerate(row):
#             if enum==0:
#                 tag = e
#             else:
#                 e=ast.literal_eval(e)
#                 arr[e[0]]=e[1]
#         inverted_index[row[0]] = arr

project_name = "#yourPhoto"
netids = ["Jake Bareket (jhb334)", "Anya Chopra (ac948)", "Michael Herbstman (mh856)", "David Miron (dm585)", "Alexandra Ward (amw349)"]

@irsystem.route('search', methods=['GET', 'POST'])
def search():
    print ("search")
    form = request.form
    form_submitted = False
    print (request.data)
    if request.method == 'POST':
        print ("Form submitted...")
        form_submitted = True
        input_query = request.form['input_query']
        # rochio(input_query,list_of_disliked_hashtags, list_of_liked_hashtags, word_to_int_dict, tag_inv_idx)
        print ("Seach input:", input_query)
        # output = input_to_tags(input_query, word_to_int_dict, post_dict, [])
        return render_template('search.html', name=project_name, netids=netids, form=form, form_submitted_status=form_submitted, output=["#1", "#2", "#3", "#4", "#5"])
    return render_template('search.html', name=project_name, netids=netids, form=form)

# if __name__ == "__main__":
    # print("reading word to int")
    # word_to_int = {}
    # with open("/../models/word_to_int.csv", 'rb') as f:
    #     mycsv = csv.reader(f, delimiter = ",")
    #     for x, row in enumerate(mycsv):
    #         if x!=0:
    #             mydict[row[0]] = int(row[1])
    # print("reading post to tags")
    # post_dict = {}
    # with open("/../models/post_dict.csv", 'rb') as f:
    #     mycsv = csv.reader(f, delimiter = ",")
    #     for x, row in enumerate(mycsv):
    #         if x!=0:
    #             mydict[row[0]] = (row[1])
    # output = input_to_tags("running with my boys and dog", word_to_int_dict, post_dict)
