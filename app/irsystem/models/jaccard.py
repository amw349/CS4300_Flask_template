from parsers_and_TFidf_setup import *

def top_jaccard_sim(post_dic, input_vec, td_mat):
    top_posts = []
    jaccard_sims = []
    scores = []

    for row in td_mat:
        num = np.sum(np.logical_and(input_vec, row))
        denom = np.sum(np.logical_or(input_vec, row))
        try:
            jaccard_sims.append(float(num) / float(denom))
        except:
            jaccard_sims.append(0)

    sorted_indicies = np.argsort(jaccard_sims)[::-1]

    for i in range(0, 5):
        if(sorted_indicies[i] in post_dic):
            top_posts.append(post_dic[sorted_indicies[i]])
            scores.append(jaccard_sims[sorted_indicies[i]])

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

def input_vec(word_to_int_dict, location, keywords):
    vec = np.zeros(len(word_to_int_dict))
    locs = re.findall('[a-z]+', location.lower())
    words = cleanup(keywords)
    for w in words:
        if w in word_to_int_dict:
            vec[word_to_int_dict[w]] = 1
    return vec

def input_to_tags(location, keywords):
    num_tags = 10
    #profile_lst = []
    # for subdir, dirs, files in os.walk('./'):
    #     for file in files:
    #         if file[(len(file)-5):(len(file))]=='.json':
    #             profile_lst.append(file)
    #print(profile_lst)
    profile_lst = ['profile_davidmiron.json', 'profile_cornellpresident.json', 'profile_alexisren.json', 'profile_nacimgoura.json', 'asos.json', 'supremenewyork.json', 'adidas.json', 'adidasoriginals.json', 'lululemon.json', 'vans.json', 'converse.json', 'underarmour.json']
    word_to_int_dict, tag_to_int_dict, int_to_word_dict, int_to_tag_dict, word_TDF,\
    tag_TDF, word_inv_idx, tag_inv_idx, post_dict = process_list_of_jsons(profile_lst)

    in_vec = input_vec(word_to_int_dict, location, keywords)

    top_jaccard_posts,scores = top_jaccard_sim(post_dict, in_vec, word_TDF)
    tags = top_n_tags(num_tags, top_jaccard_posts)
    fallback_tag_lst = fallback_tags(keywords, loc="")

    #for i in range (num_tags):
    #    if scores[i] < 1:
    #         tags[i] = fallback_tag_lst[i]
    return tags

if __name__ == "__main__":
    tags = input_to_tags("", "he may be old and he may not be a ginger")
    print(tags)
    # word_to_int_dict, tag_to_int_dict, int_to_word_dict, int_to_tag_dict, word_TDF,\
    # tag_TDF, word_inv_idx, tag_inv_idx, post_dict = process_list_of_jsons(['profile_davidmiron.json'])
    # print (post_dict)
    # word_to_int_dict, tag_to_int_dict, int_to_word_dict, int_to_tag_dict, word_TDF,\
    # tag_TDF, word_inv_idx, tag_inv_idx, post_dict = process_list_of_jsons(['profile_davidmiron.json'])
