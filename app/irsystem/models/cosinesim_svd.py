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
with open(os.getcwd()+"/app/irsystem/models/goodwords.csv") as f:
    mycsv = csv.reader(f, delimiter = ",")
    for x, row in enumerate(mycsv):
        if x!=0:
            good_tags[row[0]] = [float(row[1]), float(row[2]), float(row[3])]

def get_avglikes(tag, mydict):
    return mydict[tag][0]

def get_likescore(tag, mydict):
    val = float(mydict[tag][1])
    if val > 1:
        return round(float(val-1)*1.0, 3)
    elif val < 1:
        return round(val*-1, 3)
    elif val == 1:
        return 0

def get_totalposts(tag, mydict):
    return mydict[tag][2]

def statistics_top_hashtags(top_hashtags, mydict):
    statistics = {}
    for hshtg in top_hashtags:
        statistics[hshtg] = {"avg_likes": get_avglikes(hshtg), "like_score": get_likescore(hshtg), total_posts: get_totalposts(hshtg)}
    return statistics

def json_list():
    path_to_json_dir = os.path.dirname(os.path.abspath(_file_))+'/../../static/json'
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

def input_to_tags(input_text, word_to_int_dict, post_dict, int_to_word_dict, td_mat, words_compressed, good_tags, post_description, k=10):
    cosine_sims=[]
    top_posts=[]
    top_tags= []
    count=0
    keywords = cleanup(input_text)
    words_compressed = np.transpose(words_compressed)
    words_compressed = normalize(words_compressed, axis = 1)
    avg_input_vec = np.zeros(words_compressed.shape[1])
    # print("here1")
    for word in keywords:
        if word in word_to_int_dict:
            count = count + 1
            avg_input_vec = avg_input_vec + words_compressed[word_to_int_dict[word]]
    # print("here2")
    try:
        avg_input_vec = avg_input_vec / count
    except:
        avg_input_vec = 0

    for row in words_compressed:
        cosine_sims.append(np.dot(avg_input_vec, row))
    cosine_sims_sort = np.argsort(cosine_sims)[::-1]
    top_words = [int_to_word_dict[i] for i in cosine_sims_sort]
    top_scores = [cosine_sims[i] for i in cosine_sims_sort]

    vec = np.zeros(len(word_to_int_dict))
    for i in cosine_sims_sort[:100]:
        if int_to_word_dict[i] in word_to_int_dict:
            vec[i] = cosine_sims[i]
    # print("dot")
    post_scores = np.dot(td_mat, vec)
    # print("afterdot")
    post_arg_scores = np.argsort(post_scores)[::-1]

    tag_count = 0
    ind = 0
    last_tag_score = 0
    returning_tag_set = set()
    while (tag_count < 10):
        tag_set = post_dict[post_arg_scores[ind]]
        # descrip = post_description[post_arg_scores[ind]]
        # print(descrip)
        for tag in tag_set:
            score = post_scores[post_arg_scores[ind]]
            if score > 1:
                score = 1
            if (tag[1:] in good_tags.keys()):
                like_score = get_likescore(tag[1:], good_tags)
                if tag not in returning_tag_set:
                    # print(tag_count)
                    returning_tag_set.add(tag)
                    top_tags.append((tag, round(score, 3)))
                    tag_count += 1
                    last_tag_score = score
        ind += 1
    # print(top_tags)
    return top_tags[:10]

if __name__ == "__main__":

    int_to_word_dict = {}
    word_to_int_dict = {}
    with open("word_to_int.csv", 'rb') as f:
        mycsv = csv.reader(f, delimiter = ",")
        for x, row in enumerate(mycsv):
            if x!=0:
                word_to_int_dict[row[0]] = int(row[1])
                int_to_word_dict[int(row[1])] = row[0]

    sparse_mat = load_npz('word_TF_IDF.npz')
    word_TF_IDF = np.asarray(sparse_mat.todense())
    words_compressed = np.load('words_compressed.npy')

    post_dict = {}
    with open("post_dict.csv", 'rb') as f:
        mycsv = csv.reader(f, delimiter = ",")
        for x, row in enumerate(mycsv):
            if x!=0:
                post_dict[int(row[0])] = ast.literal_eval(row[1])

    out = input_to_tags("running on the beach in paradise", word_to_int_dict, post_dict, int_to_word_dict, word_TF_IDF, words_compressed, good_tags, k=10)
    # print (out)
