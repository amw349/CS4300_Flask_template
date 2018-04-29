from parsers_and_TFidf_setup import *
from numpy import linalg as LA
from scipy.sparse.linalg import svds
from sklearn.preprocessing import normalize

def cleanup(input_text):
    keywords = input_text.split()
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

def input_vec(td_mat, word_to_int_dict, keywords):
    vec = np.zeros(td_mat.shape[0])
    for w in keywords:
        if w in word_to_int_dict:
            vec[word_to_int_dict[w]] = 1
    return vec

def input_to_tags(input_text, td_mat, word_to_int_dict, post_dict, int_to_word_dict, k=10):
    cosine_sims=[]
    top_posts=[]
    count=0
    keywords = cleanup(input_text)
    words_compressed, x, docs_compressed = svds(td_mat.astype(float), k=2)
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

    cosine_sims = np.argsort(cosine_sims)
    top_words = [int_to_word_dict[i] for i in cosine_sims]
    vec = input_vec(td_mat, word_to_int_dict, top_words[:10])

    post_scores = []
    for i in range(0, td_mat.shape[1]):
        sim = np.dot(td_mat[:,i], vec)
        sim = sim / ((LA.norm(vec)) * (LA.norm(td_mat[:,i])))
        post_scores.append(sim)
    post_scores = np.argsort(post_scores)
    print(len(post_dict))
    top_tags = [post_dict[j]['tags'] for j in post_scores]
    return []

if __name__ == "__main__":
    word_to_int_dict, tag_to_int_dict, int_to_word_dict, int_to_tag_dict, word_TDF,\
    tag_TDF, word_inv_idx, tag_inv_idx, post_dict = process_list_of_jsons(['atighteru.json', 'balous_friends.json'])

    print(input_to_tags("", word_TDF, word_to_int_dict, post_dict, int_to_word_dict, k=10))
