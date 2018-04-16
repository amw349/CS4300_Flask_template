from Parsers_TFidf_setup import *

def top_jaccard_sim(post_dic, input_vec, td_mat):
    top_posts = []
    jaccard_sims = []
    for row in td_mat:
        jaccard_sims.append(len(np.intersect1d(input_vec, td_mat[i])) / len(np.union1d(input_vec, td_mat[i])))

    jaccard_sims = np.argsort(jaccard_sims)
    #instead of returning the raw scores, talk to jake about using an index
    #to convert the scores back into the original posts. This may involve
    #creating a separate dictionary in the function that maps post_id -> sim_score.
    for i in range(0, 10):
        top_posts.append(post_dic[jaccard_sims[i]])

    return top_posts

def top_n_tags(n, top_posts):
    tags = []
    sorted_posts = sorted(top_posts, key = lambda x : x['numberLikes'])
    for post in sorted_posts:
        for tag in post[i]['tags']:
            tags.append(tag)

    return tags[:n]

def cleanup(keywords):
    processed = []
    lst = []
    for word in keywords:
        for char in word:
            if char.isalpha():
                lst.append(i.lower())
        s = "".join(lst)
        lst = []
        processed.append(s)
    return processed

def input_vec(word_to_int_dict, location, keywords):
    vec = np.zeros(len(word_to_int_dict))
    locs = re.findall('[a-z]+', location.lower())
    words = cleanup(keywords)

    for w in words:
        if w in word_to_int_dict:
            vec[word_to_int_dict[w]] = 1

    return vec

def input_to_tags(location, keywords):
    word_to_int_dict, tag_to_int_dict, int_to_word_dict, int_to_tag_dict, word_TDF,\
    tag_TDF, word_inv_idx, tag_inv_idx, post_dict = process_list_of_jsons(['profile_davidmiron.json'])
    in_vec = input_vec(word_to_int_dict, location, keywords)
    return top_n_tags(10, top_jaccard_sim(post_dict, in_vec, word_TDF))

if __name__ == "__main__":
    word_to_int_dict, tag_to_int_dict, int_to_word_dict, int_to_tag_dict, word_TDF,\
    tag_TDF, word_inv_idx, tag_inv_idx, post_dict = process_list_of_jsons(['profile_davidmiron.json'])
