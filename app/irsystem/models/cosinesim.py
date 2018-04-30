from parsers_and_TFidf_setup import *
from numpy import linalg as LA
from scipy.sparse.linalg import svds
from sklearn.preprocessing import normalize
import csv
import os
import numpy as np

good_tags={}
# dict has keys = goodtag and values equal to list where the elements are avglikes, likescore, and totalposts

with open("goodwords.csv", 'rb') as f:
    mycsv = csv.reader(f, delimiter = ",")
    for x, row in enumerate(mycsv):
        if x!=0:
            good_tags[row[0]] = [float(row[1]), float(row[2]), float(row[3])]

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

def input_to_tags(input_text, word_to_int_dict, post_dict, int_to_word_dict, k=10):
    print("MIGHT BE WORKING")
    cosine_sims=[]
    top_posts=[]
    count=0
    keywords = cleanup(input_text)
    # docs_compressed, x, words_compressed = svds(td_mat.astype(float), k=10)
    print("MIGHT BE WORKING")
    words_compressed = np.load(os.getcwd()+'/app/irsystem/models/words_compressed.npy')
    words_compressed = normalize(words_compressed, axis = 1)
    avg_input_vec = np.zeros(words_compressed.shape[1])

    for word in keywords:
        if word in word_to_int_dict:
            count = count + 1
            avg_input_vec = avg_input_vec + words_compressed[word_to_int_dict[word]]

    try:
        avg_input_vec = avg_input_vec / count
    except:
        avg_input_vec = 0

    for row in words_compressed:
        cosine_sims.append(np.dot(avg_input_vec, row))

    cosine_sims = np.argsort(cosine_sims)[::-1]
    top_words = [int_to_word_dict[i] for i in cosine_sims]
    vec = input_vec(word_to_int_dict, top_words[:10])

    post_scores = []
    for i in range(0, td_mat.shape[0]):
        sim = np.dot(td_mat[i], vec)
        sim = sim / ((LA.norm(vec)) * (LA.norm(td_mat[i])))
        post_scores.append(sim)
    post_arg_scores = np.argsort(post_scores)[::-1]
    top_tags = [(post_dict[j], post_scores[j]) for j in post_arg_scores]
    final_lst = []
    for tup in top_tags:
        for tag in tup[0]:
            final_lst.append((tag, tup[1]))

    return final_lst[:10]

if __name__ == "__main__":
    print("reading word to int")
    word_to_int = {}
    with open("word_to_int.csv", 'rb') as f:
        mycsv = csv.reader(f, delimiter = ",")
        for x, row in enumerate(mycsv):
            if x!=0:
                mydict[row[0]] = int(row[1])
    print("reading post to tags")
    post_dict = {}
    with open("/post_dict.csv", 'rb') as f:
        mycsv = csv.reader(f, delimiter = ",")
        for x, row in enumerate(mycsv):
            if x!=0:
                mydict[row[0]] = (row[1])
    print(input_to_tags("merry christmas", word_to_int_dict, post_dict, int_to_word_dict, k=10))


#    word_to_int_dict, tag_to_int_dict, int_to_word_dict, int_to_tag_dict, \
#    word_TDF, tag_TDF, word_inv_idx, tag_inv_idx, post_dict, word_TF_IDF, doc_norms, idf_dict = process_list_of_jsons(['atighteru.json', 'balous_friends.json'])

#    print(input_to_tags("merry christmas", word_TDF, word_to_int_dict, post_dict, int_to_word_dict, k=10))
