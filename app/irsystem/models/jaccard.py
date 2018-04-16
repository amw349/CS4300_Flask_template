from parsers_and_TFidf_setup import *

def top_jaccard_sim(post_dic, input_vec, td_mat):
    # print (input_vec)
    top_posts = []
    jaccard_sims = []
    for row in td_mat:
        try:
            jaccard_sims.append(len(np.intersect1d(input_vec, row)) / len(np.union1d(input_vec, row)))
        except:
            jaccard_sims.append(0)

    jaccard_sims = np.argsort(jaccard_sims)[::-1]
    #instead of returning the raw scores, talk to jake about using an index
    #to convert the scores back into the original posts. This may involve
    #creating a separate dictionary in the function that maps post_id -> sim_score.
    for i in range(0, 10):
        if(jaccard_sims[i] in post_dic):
            top_posts.append(post_dic[jaccard_sims[i]])

    return top_posts

def top_n_tags(n, top_posts):
    tags = []
    #print (top_posts)
    sorted_posts = sorted(top_posts, key = lambda x : x['numberLikes'], reverse=True)
    for post in sorted_posts:
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

def input_vec(word_to_int_dict, location, keywords):
    vec = np.zeros(len(word_to_int_dict))
    locs = re.findall('[a-z]+', location.lower())
    # print ("input before cleanup:", keywords)
    words = cleanup(keywords)
    # print ("input after cleanup:", words)
    for w in words:
        # print ("w in words:", w)
        if w in word_to_int_dict:
            vec[word_to_int_dict[w]] = 1
    return vec

def input_to_tags(location, keywords):
    word_to_int_dict, tag_to_int_dict, int_to_word_dict, int_to_tag_dict, word_TDF,\
    tag_TDF, word_inv_idx, tag_inv_idx, post_dict = process_list_of_jsons(['profile_davidmiron.json'])

    in_vec = input_vec(word_to_int_dict, location, keywords)
    return top_n_tags(10, top_jaccard_sim(post_dict, in_vec, word_TDF))

# if __name__ == "__main__":
# #He may be old and he may not be a ginger but he is my brother #nofilter #goodvibesonly
#     tags = input_to_tags("", ["he", "may", "be", "old", "and", "he", "may", "not", "be", "a", "ginger"])
#     print(tags)
    #word_to_int_dict, tag_to_int_dict, int_to_word_dict, int_to_tag_dict, word_TDF,\
    #tag_TDF, word_inv_idx, tag_inv_idx, post_dict = process_list_of_jsons(['profile_davidmiron.json'])
    #print (post_dict)
    #word_to_int_dict, tag_to_int_dict, int_to_word_dict, int_to_tag_dict, word_TDF,\
    #tag_TDF, word_inv_idx, tag_inv_idx, post_dict = process_list_of_jsons(['profile_davidmiron.json'])
