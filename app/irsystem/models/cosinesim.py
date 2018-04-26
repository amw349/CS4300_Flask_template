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

def top_n_tags(top_posts, n=10):
    tags = []
    for post in top_posts:
        for tag in post['tags']:
            tags.append(tag)
    return tags[:n]

def input_to_tags(input_text, word_to_int_dict, post_dict, k=10):
    cosine_sims=[]
    top_posts=[]
    count=0
    keywords = cleanup(input_text)
    words_compressed, x, docs_compressed = svds(td_mat, k=k)
    words_compressed = normalize(words_compressed, axis = 1)
    avg_input_vec = np.zeros(10)

    for word in keywords:
        if word in word_to_int_dict:
            count = count + 1
            avg_input_vec = avg_input_vec + words_compressed[word_to_int_dict[word]]
    avg_input_vec = avg_input_vec / count

    for row in words_compressed:
        cosine_sims.append(np.dot(avg_input_vec, row))

    cosine_sims = np.argsort(cosine_sims)
    top_posts = [post_dict[i] for i in cosine_sims]

    return top_n_tags(top_posts)

if __name__ == "__main__":
    profile_lst = ['profile_davidmiron.json', 'profile_cornellpresident.json', 'profile_alexisren.json', 'profile_nacimgoura.json', 'asos.json', 'supremenewyork.json', 'adidas.json', 'adidasoriginals.json', 'nikelab.json', 'nike.json', 'lululemon.json', 'vans.json', 'converse.json', 'underarmour.json', 'google.json', 'amazon.json', 'apple.json', 'samsungus.json']
    word_to_int_dict, tag_to_int_dict, int_to_word_dict, int_to_tag_dict, word_TDF,\
    tag_TDF, word_inv_idx, tag_inv_idx, post_dict = process_list_of_jsons(profile_lst)
    print(closest_tags("cornell technology achievement science", word_TDF, word_to_int_dict, post_dict))
