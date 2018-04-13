#!/usr/bin/env python
import json
import numpy as np
import re


"""takes in a list of strings representing
json objects (which must be in the current directory)
and treats each post like a document. Returns a
dictionary of words to word indicies in the vector representation
of our data. Also return a term document matric of the entrue data set

returns: word_to_int_dict           maps words to an index in a word vector
        tag_to_int_dict             maps words to an index in a tag vector
        int_to_word_dict            maps indicies to words in a word vector
        int_to_tag_dict             maps indicies to words in a word vector
        word_TDF
        tag_TDF
        word_inv_idx
        tag_inv_idx
        post_dict
"""
#in the future chage the argument to a path and use os.listdir(path)
def process_list_of_jsons(lst_of_jsons):
    #get the set of all words and a seperate set of all tags
    #also put every post a in post dict and assign it a number
    post_dict = {}
    word_set = set()
    tag_set = set()
    post_count = 0
    for json_name in lst_of_jsons:
        data = json.load(open(json_name))
        posts = data['posts']
        for post in posts:
            post_count += 1#posts with no tags or captions still included
            try:
                post_dict[post_count] = post
                description = post['description']
                tags = post['tags']

                tokenized_description = prepareDescription(description)
                if len(tags) != 0:#don't count posts with no tags at least for now
                    for d_token in tokenized_description:
                        word_set.add(d_token)
                    for t_token in tags:
                        tag_set.add(prepareTag(t_token))
            except:
                pass
    num_posts = post_count
    
    #create dictionaries for the vector index of each word
    sorted_words = sorted(word_set) 
    sorted_tags = sorted(tag_set)

    word_to_int_dict = {} 
    int_to_word_dict = {}
    tag_to_int_dict = {}
    int_to_tag_dict = {}
    
    for i in range (len(sorted_words)):
        if sorted_words[i] != " " and sorted_words[i] != "":
            word_to_int_dict[sorted_words[i]]=i
            int_to_word_dict[i]=sorted_words[i]
    for i in range (len(sorted_tags)):
        if sorted_words[i] != " " and sorted_words[i] != "":
            tag_to_int_dict[sorted_tags[i]]=i
            int_to_tag_dict[i]=sorted_tags[i]
    #now go back and create the TFidf as well as the inverted index 
    #print (num_posts)
    num_words = len(word_to_int_dict)
    num_tags = len(tag_to_int_dict)
    word_TDF = np.zeros((num_posts,num_words))
    tag_TDF = np.zeros((num_posts,num_tags))
    
    word_inv_idx = [list([]) for _ in xrange(num_words)] #use this if in for python3 [[] for _ in range(num_words)]
    tag_inv_idx = [list([]) for _ in xrange(num_tags)] #use this if in for python3 [[] for _ in range(num_tags)]
    
    post_counter = 0
    for json_name in lst_of_jsons:
        data = json.load(open(json_name))
        posts = data['posts']
        for post in posts:
            try:
                post_counter += 1
                description = post['description']
                tags = post['tags']
                tokenized_description = prepareDescription(description)
                if len(tags) != 0:#don't count posts with no tags at least for this application
                    for d_token in tokenized_description:
                        if d_token in word_to_int_dict:
                            word_TDF[post_counter,word_to_int_dict[d_token]] = 1
                            #Adds the current post to the list of posts matched to that word
                            word_inv_idx[word_to_int_dict[d_token]].append(post_counter)
                    for t_token in tags:
                        t_token = prepareTag(t_token)#remove the leading hashtag
                        if d_token in word_to_int_dict:
                            tag_TDF[post_counter,tag_to_int_dict[t_token]] = 1
                            #Adds the current post index to the list of posts matched to that word
                            tag_inv_idx[tag_to_int_dict[t_token]].append(post_counter)
            except:
                pass
    return word_to_int_dict, tag_to_int_dict, int_to_word_dict, int_to_tag_dict, \
    word_TDF, tag_TDF, word_inv_idx, tag_inv_idx, post_dict

"takes the text and returns a list of strings"
def prepareDescription(text):
    text = removeEmojies(text)
    text = strip_links(text)
    text = removeNonAlpha(text)
    return text

def removeEmojies(text):
    emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                       "]+", flags=re.UNICODE)

    clean = (emoji_pattern.sub(r'', text)) # no emoji
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
    s = "".join(lst)
    x = 7
    return s.split(' ')

    #removes the hashtag
def prepareTag(tag):
    return tag[1:].lower()
    
# def strip_all_entities(text):
#     entity_prefixes = ['@','#']
#     for separator in  string.punctuation:
#         if separator not in entity_prefixes :
#             text = text.replace(separator,' ')
#     words = []
#     for word in text.split():
#         word = word.strip()
#         if word:
#             if word[0] not in entity_prefixes:
#                 words.append(word)
#     return ' '.join(words)

if __name__ == "__main__":
    word_to_int_dict, tag_to_int_dict, int_to_word_dict, int_to_tag_dict, word_TDF,\
    tag_TDF, word_inv_idx, tag_inv_idx, post_dict = process_list_of_jsons(['profile_davidmiron.json'])
    
    """some test code. You will want to use int_to_word_dict to get printouts that make sense instead of 0s and 1s"""
    #print (word_to_int_dict)
    #print (post_dict)
    print (word_TDF[1])
    #print (word_TDF[2])
    print (post_dict[1])
    for i in range(len(word_TDF[1])):
        if word_TDF[1][i] != 0:
            print (int_to_word_dict[i])
    
    x=21
    print (tag_TDF)
    print (tag_TDF[x])
    #print (word_TDF[2])
    print (post_dict[x])
    for i in range(len(tag_TDF[x])):
        if tag_TDF[x][i] != 0:
            print (int_to_tag_dict[i]) 
