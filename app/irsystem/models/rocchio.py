def get_related_docs_vec(tag_lst,num_words,tag_inv_idx):
    new = np.zeros(num_words)
    for tag in tag_lst:
        if tag in tag_inv_idx:
            new+=tag_inv_idx[tag]
    return new

def input_vec(word_to_int_dict):
    vec = np.zeros(td_mat.shape[1])
    for w in keywords:
        if w in word_to_int_dict:
            vec[word_to_int_dict[w]] = 1
    return vec

def rochio(original_input, list_of_liked_hashtags, word_to_int_dict, tag_inv_idx):
    a=.8
    b=.2
    num_words = len(word_to_int_dict)
    original_query_vec = input_vec(original_query.split(' '))
    good_docs_sum_vec = get_related_docs_vec(list_of_liked_hashtags,num_words, tag_inv_idx)
    newQ = a*original_query_vec+ b*good_docs_sum_vec

    return newQ #in the flask you will feed this back to the input_to_tags func
