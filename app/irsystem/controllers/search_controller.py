from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.cosinesim_svd import input_to_tags
from app.irsystem.models.parsers_and_TFidf_setup import process_list_of_jsons
from numpy import linalg as LA
from scipy.sparse.linalg import svds
import os
import ast
import csv
from sklearn.preprocessing import normalize
from scipy.sparse import load_npz
import ast
import operator

project_name = "#yourPhoto"
netids = ["Jake Bareket (jhb334)", "Anya Chopra (ac948)", "Michael Herbstman (mh856)", "David Miron (dm585)", "Alexandra Ward (amw349)"]

sparse_mat = load_npz('app/irsystem/models/word_TF_IDF.npz')
word_TF_IDF = np.asarray(sparse_mat.todense())

words_compressed = np.load('app/irsystem/models/words_compressed.npy')

post_dict = {}
with open("app/irsystem/models/post_dict.csv", 'rb') as f:
    mycsv = csv.reader(f, delimiter = ",")
    for x, row in enumerate(mycsv):
        if x!=0:
            post_dict[int(row[0])] = ast.literal_eval(row[1])

# inverted_index_dict = {}
# with open("app/irsystem/models/inverted_index_new.csv", 'rb') as f:
#     mycsv = csv.reader(f, delimiter = ",")
#     for x, row in enumerate(mycsv):
#         if x!=0:
#             post_dict[str(row[0])] = str(row[1])

post_description = {}
with open("app/irsystem/models/post_dict_description.csv", 'rb') as f:
    mycsv = csv.reader(f, delimiter = ",")
    for x, row in enumerate(mycsv):
        if x!=0:
            post_dict[int(row[0])] = ast.literal_eval(row[1])

word_to_int_dict = {}
int_to_word_dict = {}
with open("app/irsystem/models/word_to_int.csv", 'rb') as f:
    mycsv = csv.reader(f, delimiter = ",")
    for x, row in enumerate(mycsv):
        if x!=0:
            word_to_int_dict[str(row[0])] = int(row[1])
            int_to_word_dict[int(row[1])] = row[0]

post_dict = {}
with open("app/irsystem/models/post_dict.csv", 'rb') as f:
    mycsv = csv.reader(f, delimiter = ",")
    for x, row in enumerate(mycsv):
        if x!=0:
            post_dict[int(row[0])] = ast.literal_eval(row[1])

sparse_mat = load_npz('app/irsystem/models/word_TDF.npz')
TF_IDF_matrix = np.asarray(sparse_mat.todense())

good_tags = {}
with open("app/irsystem/models/goodwords.csv") as f:
    mycsv = csv.reader(f, delimiter = ",")
    for x, row in enumerate(mycsv):
        if x!=0:
            good_tags[row[0]] = [float(row[1]), float(row[2]), float(row[3])]

def get_avglikes(tag):
    if tag not in good_tags:
        return 0
    return good_tags[tag][0]

def get_likescore(tag):
    if tag not in good_tags:
        return 0
    else:
        val = float(good_tags[tag][1])
        if val > 1:
            return round(float(val-1)*1.0, 3)
        elif val < 1:
            return round(val*-1, 3)
        elif val == 1:
            return 0

def get_totalposts(tag):
    if tag not in good_tags:
        return 0
    else:
        return good_tags[tag][2]

def statistics_top_hashtags(top_hashtags):
    statistics = {}
    for hashtag_sim_tuple in top_hashtags:
        avg_likes = get_avglikes(hashtag_sim_tuple[0][1:])
        like_score = get_likescore(hashtag_sim_tuple[0][1:])
        total_posts = get_totalposts(hashtag_sim_tuple[0][1:])
        statistics[hashtag_sim_tuple[0][1:]] = {"avg_likes": avg_likes, "like_score": like_score, "total_posts": total_posts}
    return statistics

@irsystem.route('search', methods=['GET', 'POST'])
def search():
    # print ("search")
    form = request.form
    form_submitted = False
    # print (request.data)
    if request.method == 'POST':
        # print ("Form submitted...")
        form_submitted = True
        input_query = request.form['input_query']
        # rochio(input_query,list_of_disliked_hashtags, list_of_liked_hashtags, word_to_int_dict, tag_inv_idx)
        # print ("Seach input:", input_query)
        output = input_to_tags(input_query, word_to_int_dict, post_dict, int_to_word_dict, word_TF_IDF, words_compressed, good_tags, post_description)
        # print ("Output:", output)
        statistics = statistics_top_hashtags(output)
        # print ("statistics:", statistics)
        return render_template('search.html', name=project_name, netids=netids, form=form, form_submitted_status=form_submitted, input_query=input_query, output=output, statistics=statistics)
    return render_template('search.html', name=project_name, netids=netids, form=form)


@irsystem.route('rocchio', methods=['GET'])
def rocchio():
    if request.method == 'GET':
        form = request.form
        print ("rocchio")
        print ("request:", request.args)
        print ("input", request.args['input'])
        print ("hashtag1", request.args['hashtag1'])
        print ("hashtag2", request.args['hashtag2'])
        # input = request.args['input']
        # likes = request.args['likes']
        results = [("these", 10), ("are", 9), ("the", 8), ("results", 7)]
        print ("got this far! keep going")
        print ("form:", form)
        return render_template('search.html', name=project_name, netids=netids, form=form, results=results)
