#!/usr/bin/env python
import json
import numpy as np
import re
import os
import math

"""takes in a list of strings representing
json objects (which must be in the current directory)
and treats each post like a document. Returns a
dictionary of words to word indicies in the vector representation
of our data. Also return a term document matric of the entrue data set

returns:
        word_to_int_dict           maps words to an index in a word vector
        tag_to_int_dict             maps words to an index in a tag vector
        int_to_word_dict            maps indicies to words in a word vector
        int_to_tag_dict             maps indicies to words in a word vector
        word_TDF                    a matrix where the columns are individual posts and the rows are binary
                                        values of whether or not the word is in that post
        tag_TDF                     same thing as word_TDF but for tags
        word_inv_idx                an inverted index of words to post numbers
        tag_inv_idx                 an inverted index of tags to posts numbers
        post_dict                   maps indicies to their corresponding post
        word_TF_IDF                 a matrix where the columns are individual posts and the rows are binary
                                        values of whether or not the word is in that post
        doc_norms                   maps doc index to the norm of that docment
        idf_dict                    maps words to their IDF score (score is high if a word appears in many docs)
        
        not included for now
        #word_post_vec_inv_idx       an inverted index of words to vectorized posts


"""
#To do: filter words used only by a single profile

def fallback_tags(lst_of_wrds, loc=""):
    tags = []
    n = len(lst_of_wrds)
    if n > 2: n = 2
    for word in lst_of_wrds:
        tags.append("#"+word)
    if loc == "":
        return tags[0:n]
    else:
        return tags[0:n-1] + [loc]

#in the future chage the argument to a path and use os.listdir(path)
def process_list_of_jsons(lst_of_jsons):
    #get the set of all words and a seperate set of all tags
    #also put every post a in post dict and assign it a number
    basedir = os.getcwd()+'/../../../app/static/json/'
    post_dict = {}
    word_set = set()
    tag_set = set()
    word_freq_dict = {}
    num_jsons_tag_appears_in = {}
    post_count = 0
    bad_words = {'',' ','  ', ',' '!', 'a', 'about','above','after','again','against','all','am','an','and','any',\
                 'are','aren','as','at','be','because','been','before','being','below','between',\
                 'both','but','by','can','cannot','could','couldn','did','didn','do','does','doesn',\
                 'doing','don','down','during','each','few','for','from','further','had','hadn','has',\
                 'hasn','have','haven','having','he','here','hers','herself','him','himself','his','how',\
                 't','i','d','ll','m','ve','if','in','into','is','isn','it','its','itself','let','me','more',\
                 'most','mustn','my','myself','no','nor','not','of','off','on','once','only','or','other',\
                 'ought','our','ours','ourselves','out','over','own','same','shan','she','should','shouldn',\
                 'so','some','such','than','that','the','their','theirs','them','themselves','then','there',\
                 'they','this','those','through','to','too','under','until','up','very','was','wasn','we',\
                 'were','weren','what','what','when','where','which','while','who','whom','why','with','won',\
                 'would','wouldn','you','your','yours','yourself', 'yourselves'}
    
    for json_name in lst_of_jsons:
        
        data = {}
        json_tag_set = set()
        with open(basedir+json_name) as f:
            data = json.load(f)
        posts = data['posts']
        
        for post in posts:
            #posts with no tags or captions still included
            try:
                description = post['description']
                tags = post['tags']
                
                tokenized_description = prepareDescription(description)
                if len(tags) != 0:#don't count posts with no tags at least for now
                    for d_token in tokenized_description:
                        if d_token not in bad_words:
                            
                            word_set.add(d_token)
                                
                            if d_token in word_freq_dict:
                                word_freq_dict[d_token] += 1
                            else:
                                word_freq_dict[d_token]=1
                                
                                
                    for t_token in tags:
                        tag_set.add(prepareTag(t_token))
                        json_tag_set.add(prepareTag(t_token))
                    post_dict[post_count] = post
                    post_count += 1
            except:
                #print ("----failed")
                pass
        for tag in json_tag_set:
            if tag in num_jsons_tag_appears_in:
                num_jsons_tag_appears_in[tag]+=1
            else:
                num_jsons_tag_appears_in[tag]=1
            
    num_posts = post_count
    #create dictionaries for the vector index of each word
    #print(num_jsons_tag_appears_in)
    for tag in num_jsons_tag_appears_in:
        if num_jsons_tag_appears_in[tag]>1:
            tag_set.add(tag)
    
    sorted_words = sorted(word_set)
    sorted_tags = sorted(tag_set)

    word_to_int_dict = {}
    int_to_word_dict = {}
    tag_to_int_dict = {}
    int_to_tag_dict = {}

    i=-1
    for word in sorted_words:
        i+=1
        word_to_int_dict[word]=i
        int_to_word_dict[i]=word   
    i=-1
    for tag in sorted_tags:
        if tag != " " and tag != "":
            i+=1
            tag_to_int_dict[tag]=i
            int_to_tag_dict[i]=tag
    #now go back and create the TFidf as well as the inverted index

    num_words = len(word_to_int_dict)
    num_tags = len(tag_to_int_dict)
    word_TDF = np.zeros((num_posts,num_words))
    tag_TDF = np.zeros((num_posts,num_tags))
    word_TF_IDF = np.zeros((num_posts,num_words))
    
    idf_dict = computeIDF_dict(word_freq_dict, num_posts)
    # idf_array = computeIDF_array(word_freq_dict, int_to_word_dict, num_posts)

    #create the empty word_inv_idx
    #word_inv_idx = [[] for _ in range(num_words)] #use this if in for python3 
    #tag_inv_idx = [[] for _ in range(num_tags)] #use this if in for python3
    word_inv_idx = [list([]) for _ in xrange(num_words)] 
    tag_inv_idx = [list([]) for _ in xrange(num_tags)]
    doc_norms = np.zeros(num_posts)
    #print (idf)
    post_counter = 0
    for json_name in lst_of_jsons:
        data = {}
        with open(basedir+json_name) as f:
            data = json.load(f)
        posts = data['posts']
        for post in posts:
            try:
                description = post['description']
                tags = post['tags']
                tokenized_description = prepareDescription(description)

                idf_score_sq_sum = 0
                if len(tags) != 0:#don't count posts with no tags at least for this application
                    for d_token in tokenized_description:
                        if d_token in idf_dict:
                            word_TDF[post_counter,word_to_int_dict[d_token]] = 1
                            
                            #Adds the current post to the list of posts matched to that word
                            word_inv_idx[word_to_int_dict[d_token]].append(post_counter)
                            idf_score_sq_sum += idf_dict[d_token]**2
                            
                            word_TF_IDF[post_counter,word_to_int_dict[d_token]] = idf_dict[d_token]
                            
                    for t_token in tags:
                        t_token = prepareTag(t_token)#remove the leading hashtag
                        if d_token in tag_to_int_dict:
                            tag_TDF[post_counter,tag_to_int_dict[t_token]] = 1
                            #Adds the current post index to the list of posts matched to that word
                            
                            tag_inv_idx[tag_to_int_dict[t_token]].append(post_counter)
                    doc_norms[post_counter] = math.sqrt(idf_score_sq_sum)
                    post_counter += 1
            except TypeError as e:
                pass
    #print (doc_norms)
    for x in word_TF_IDF:
         for y in x:
             print (x)
    #print (len(idf_dict))
    return word_to_int_dict, tag_to_int_dict, int_to_word_dict, int_to_tag_dict, \
    word_TDF, tag_TDF, word_inv_idx, tag_inv_idx, post_dict, word_TF_IDF, doc_norms, idf_dict

"takes the text and returns a list of strings"
def prepareDescription(text):
    #print ("remove emogies started")
    text = removeEmojies(text)
    #print ("strip links started")
    text = strip_links(text)
    #print ("removeNonAlpha")
    text = removeNonAlpha(text)
    return text

def removeEmojies(text):
    emoji_pattern = re.compile("["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
                       "]+", flags=re.UNICODE)
    #emoji_pattern= re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)

    #print (text)
    clean =emoji_pattern.sub(r'', text) # no emoji
    return clean

def strip_links(text):
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')
    return text

def removeNonAlpha(text):
    #m = re.match((r"([a-zA-Z]*)"), "a@!# clean&#@string")
    #g = m.groups()
    #print g
    #return g
    lst = []
    for i in text:
        if i.isalpha():
            lst.append(i.lower())
        else:
            lst.append(" ")
    s = str("".join(lst))
    x = 7
    return s.split(' ')

    #removes the hashtag
def prepareTag(tag):
    return tag[1:].lower()

#returns a dict of words to their IDF scores (eg. idf['dog']=.2)
def computeIDF_dict(word_freq_dict, num_docs, min_df=1, max_df_ratio=0.95):
    idf={}
    # YOUR CODE HERE
    for key in word_freq_dict:
        word_freq = word_freq_dict[key]
        if word_freq>=min_df and word_freq/num_docs<=max_df_ratio:
            N_over_1_plus_word_freq = num_docs/float(1+word_freq)
            IDFscore = math.log(N_over_1_plus_word_freq,2)
            idf[key]=IDFscore
    return idf

# def computeIDF_array(word_freq_dict, int_to_word_dict, num_docs, min_df=1, max_df_ratio=0.95):
#     
#     num_words = len(int_to_word_dict)
#     idf_array=np.zeros(num_words)
#     # YOUR CODE HERE
#     for i in range(num_words):
#         word_freq = word_freq_dict[int_to_word_dict[i]]
#         if word_freq>=min_df and word_freq/num_docs<=max_df_ratio:
#             N_over_1_plus_word_freq = num_docs/float(1+word_freq)
#             IDFscore = math.log(N_over_1_plus_word_freq,2)
#             idf_array[i]=IDFscore
#     return idf_array

#if __name__ == "__main__":
#    word_to_int_dict, tag_to_int_dict, int_to_word_dict, int_to_tag_dict, \
#    word_TDF, tag_TDF, word_inv_idx, tag_inv_idx, post_dict, word_TF_IDF, doc_norms, idf_dict = process_list_of_jsons(['profile_davidmiron.json'])#, 'amandabisk.json'])#, 'andyspeer.json', 'profile_alexisren.json'])

    #print(doc_norms)
#     
#     """some test code. You will want to use int_to_word_dict to get printouts that make sense instead of 0s and 1s"""
    #print (word_to_int_dict)
    #print (post_dict)
    #print (word_TDF[1])
    #print (word_TDF[2])
    # print (post_dict[1])
    # for i in range(len(word_TDF[1])):
    #     if word_TDF[1][i] != 0:
    #         print (int_to_word_dict[i])
    #
    # x=21
    # print (tag_TDF)
    # print (tag_TDF[x])
    # #print (word_TDF[2])
    # print (post_dict[x])
    # for i in range(len(tag_TDF[x])):
    #     if tag_TDF[x][i] != 0:
    #         print (int_to_tag_dict[i])


