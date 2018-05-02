from parsers_and_TFidf_setup import *
from numpy import linalg as LA
from scipy.sparse.linalg import svds
from sklearn.preprocessing import normalize
from scipy.sparse import load_npz
import csv
import os
import numpy as np
import ast

good_tags={}
# dict has keys = goodtag and values equal to list where the elements are avglikes, likescore, and totalposts

# with open("goodwords.csv") as f:
#     mycsv = csv.reader(f, delimiter = ",")
#     for x, row in enumerate(mycsv):
#         if x!=0:
#             good_tags[row[0]] = [float(row[1]), float(row[2]), float(row[3])]

def get_avglikes(tag):
    return mydict[tag][0]

def get_likescore(tag):
    val = float(mydict[tag][1])
    if val > 1:
        return float(val-1)*1.0
    elif val < 1:
        return val*-1
    elif val == 1:
        return 0

def get_totalposts(tag):
    return mydict[tag][2]

def statistics_top_hashtags(top_hashtags):
    statistics = {}
    for hshtg in top_hashtags:
        statistics[hshtg] = {"avg_likes": get_avglikes(hshtg), "like_score": get_likescore(hshtg), total_posts: get_totalposts(hshtg)}
    return statistics

def json_list():
    path_to_json_dir = os.path.dirname(os.path.abspath(__file__))+'/../../static/json'
    for _, _, filenames in os.walk(path_to_json_dir):
        return filenames

def top_cosine_sim(post_dic, input_vec, td_mat):
    top_posts = []
    cosine_sims = []
    scores = []

    for row in td_mat:
        num = np.dot(input_vec, row)
        denom = (LA.norm(input_vec))*(LA.norm(row))
        try:
            cosine_sims.append(float(num) / float(denom))
        except:
            cosine_sims.append(0)

    sorted_indicies = np.argsort(cosine_sims)[::-1]

    for i in range(0, 5):
        if(sorted_indicies[i] in post_dic):
            top_posts.append(post_dic[sorted_indicies[i]])
            scores.append(cosine_sims[sorted_indicies[i]])

    return top_posts,scores

def top_n_tags(n, top_posts):
    tags = []
        #sorted_posts = reversed(sorted(top_posts, key = lambda x : x['numberLikes']))
    for post in top_posts:
        for tag in post['tags']:
            tags.append(tag)
    return tags[:n]

def cleanup(keywords):
    keywords = keywords.split()
    processed = []
    lst = []
    for word in keywords:
        for char in word:
            if char.isalpha():
                lst.append(char.lower())
        s = "".join(lst)
        lst = []
        processed.append(s)
    return processed

def top_n_tags(top_posts, int_to_word_dict, n=10):
    words = []
    for word in top_posts:
        words.append(int_to_word_dict)

    return words[:10]

def input_vec(word_to_int_dict, keywords):
    vec = np.zeros(len(word_to_int_dict))
    for w in keywords:
        if w in word_to_int_dict:
            vec[word_to_int_dict[w]] = 1
    return vec

def pp(v,int_to_word_dict):
    lst = []
    for count, x in enumerate(v):
        if x!=0:
            lst.append(int_to_word_dict[count])
    print (lst)

def serve_jsons():

    path_to_json_dir = os.getcwd()+'/../../static/json/'
    print ("path:", os.getcwd())
    print (path_to_json_dir)
    for _, _, filenames in os.walk(path_to_json_dir):
        json_files = [ f for f in filenames if f.endswith("json") ]
    return json_files

def input_to_tags(input_text, td_mat, word_to_int_dict, post_dict, int_to_word_dict, k=10):
    cosine_sims=[]
    top_posts=[]
    top_tags = []
    count=0
    keywords = cleanup(input_text)
    v = input_vec(word_to_int_dict, keywords)
    pp(v, int_to_word_dict)
    v = v/LA.norm(v)#don't need to normalize input vec but make outputs understandable
    cosine_sims = np.dot(td_mat, v)
    cosine_sims_idxs = np.argsort(cosine_sims)[::-1]
    top_tag_lists = []

    pp(td_mat[cosine_sims_idxs[0]] ,int_to_word_dict)#prints the words coresponding to the top post
    
    best_score_and_best_coments = [(cosine_sims[cosine_sims_idxs[0]], post_dict[cosine_sims_idxs[0]]), \
                   (cosine_sims[cosine_sims_idxs[1]], post_dict[cosine_sims_idxs[1]]), \
                   (cosine_sims[cosine_sims_idxs[2]], post_dict[cosine_sims_idxs[2]]), \
                   (cosine_sims[cosine_sims_idxs[3]], post_dict[cosine_sims_idxs[3]]), \
                   (cosine_sims[cosine_sims_idxs[4]], post_dict[cosine_sims_idxs[4]])]
    return best_score_and_best_coments

    #pp(td_mat[cosine_sims_idxs[0]] ,int_to_word_dict)
    
    
    # for e in cosine_sims_new:
    #     for tag in post_dict[e]:
    #         if tag[1:] in good_tags:
    #             print("here")
    #             top_tag_lists.append(tag)

    # while(len(top_tags)<10):
    #     print("here")
    #     for tag in top_tag_lists:
    #         print("here2")
    #         if tag not in top_tags:
    #             top_tags.append(tag)
    #print(top_tag_lists[:10])


if __name__ == "__main__":
    word_to_int_dict, tag_to_int_dict, int_to_word_dict, int_to_tag_dict, \
    word_TDF, tag_TDF, word_inv_idx, tag_inv_idx, post_dict, word_TF_IDF, doc_norms, idf_dict = process_list_of_jsons(serve_jsons())
    print ("finished pre processing")
    k = input_to_tags("my addorable cat loves his belly rubs",  word_TF_IDF, word_to_int_dict, post_dict, int_to_word_dict, k=10)
    for e in k:
        print (e)
           
    print ('')
    k = input_to_tags("running through the park with my dog and favorite playlist",  word_TF_IDF, word_to_int_dict, post_dict, int_to_word_dict, k=10)
    for e in k:
        print (e)
        
    k = input_to_tags("eat food steak burger tasty yum shake chicken",  word_TF_IDF, word_to_int_dict, post_dict, int_to_word_dict, k=10)
    for e in k:
        print (e)
# def pp(v,int_to_word_dict):
#     lst = []
#     for count, x in enumerate(v):
#         if x!=0:
#             lst.append(int_to_word_dict[count])
#     print (lst)
# 
# def input_to_tags(input_text, td_mat, word_to_int_dict, post_dict, int_to_word_dict, k=10):
#     cosine_sims=[]
#     top_posts=[]
#     top_tags = []
#     count=0
#     keywords = cleanup(input_text)
#     v = input_vec(word_to_int_dict, keywords)
#     pp(v, int_to_word_dict)
#     v = v/LA.norm(v)#don't need to normalize input vec but make outputs understandable
#     cosine_sims = np.dot(td_mat, v)
#     cosine_sims_idxs = np.argsort(cosine_sims)[::-1]
#     top_tag_lists = []
# 
#     pp(td_mat[cosine_sims_idxs[0]] ,int_to_word_dict)#prints the words coresponding to the top post
#     
#     best_score_and_best_coments = [(cosine_sims[cosine_sims_idxs[0]], post_dict[cosine_sims_idxs[0]]), \
#                    (cosine_sims[cosine_sims_idxs[1]], post_dict[cosine_sims_idxs[1]]), \
#                    (cosine_sims[cosine_sims_idxs[2]], post_dict[cosine_sims_idxs[2]]), \
#                    (cosine_sims[cosine_sims_idxs[3]], post_dict[cosine_sims_idxs[3]]), \
#                    (cosine_sims[cosine_sims_idxs[4]], post_dict[cosine_sims_idxs[4]])]
#     return best_score_and_best_coments
# 
# 
# if __name__ == "__main__":
#     #print("reading word to int")
#     word_to_int_dict = {}
#     int_to_word_dict = {}
#     with open("word_to_int.csv", 'rb') as f:
#         mycsv = csv.reader(f, delimiter = ",")
#         for x, row in enumerate(mycsv):
#             if x!=0:
#                 word_to_int_dict[row[0]] = int(row[1])
#                 int_to_word_dict[int(row[1])] = row[0]
#     #print("reading post to tags")
#     post_dict = {}
#     with open("post_dict.csv", 'rb') as f:
#         mycsv = csv.reader(f, delimiter = ",")
#         for x, row in enumerate(mycsv):
#             if x!=0:
#                 post_dict[int(row[0])] = ast.literal_eval(row[1])
#     sparse_mat = load_npz('word_TDF.npz')
#     TF_IDF_matrix = np.asarray(sparse_mat.todense())
#     print(input_to_tags("long day in the gym", TF_IDF_matrix, word_to_int_dict, post_dict, int_to_word_dict, k=10))
