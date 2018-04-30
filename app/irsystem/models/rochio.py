def get_related_docs_vec(tag_lst,num_words,tag_inv_idx):
    new = np.zeros(num_words)
    for tag in tag_lst:
        if tag in tag_inv_idx:
            new+=tag_inv_idx[tag]
    return new

def input_vec(word_to_int_dict, keywords):
    vec = np.zeros(td_mat.shape[1])
    for w in keywords:
        if w in word_to_int_dict:
            vec[word_to_int_dict[w]] = 1
    return vec
  
def rochio(original_query_lst,list_of_disliked_hashtags, list_of_liked_hashtags, word_to_int_dict, tag_inv_idx):
    a=.5
    b=.2
    c=.3
    num_words = len(word_to_int_dict)
    original_query_vec = input_vec(original_query)
    good_docs_sum_vec = get_related_docs_vec(list_of_liked_hashtags,num_words, tag_inv_idx)
    bad_doc_sum_vec = get_related_docs_vec(list_of_disliked_hashtags,num_words, tag_inv_idx)
    newQ = a*original_query_vec+ b*good_docs_sum_vec + c*bad_doc_sum_vec
    
    
    print ("running rochio")
    
    

