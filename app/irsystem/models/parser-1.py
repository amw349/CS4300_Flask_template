import csv
import os
import json
import numpy as np
import re
import math

int_to_word_dict = {}
post_dict = {}


def serve_jsons():
    path_to_json_dir = os.getcwd()+'/../../static/json/'
    for _, _, filenames in os.walk(path_to_json_dir):
        json_files = [ f for f in filenames if f.endswith("json") ]
    return json_files

def process_list_of_jsons(lst_of_jsons):
    #get the set of all words and a seperate set of all tags
    #also put every post a in post dict and assign it a number
    basedir = os.getcwd()+'/../../../app/static/json/'
    post_count = 0
    real_data = {}
    word_set = set()
    tag_set = set()
    word_freq_dict = {}
    num_jsons_tag_appears_in = {}
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
        json_tag_set = set()
        with open(basedir+json_name) as f:
            data = json.load(f)
        posts = data['posts']
        try :
            for post in posts:
                description = post['description']
                tags = post['tags']
                post_dict[post_count] = tags
                post_count+=1
                tokenized_description = prepareDescription(description)
                if len(tags) != 0:#don't count posts with no tags at least for now
                    for d_token in tokenized_description:
                        if d_token not in bad_words:
                            word_set.add(d_token)
                likes = post['likes']
                author = json_name
                for x, tag in enumerate(tags):
                    tmp = str(tag)
                    tags[x] = tmp[1:]
                if author in real_data:
                    real_data[author].append((likes,tags))
                else:
                    real_data[author] = [(likes,tags)]
        except :
            pass
    sorted_words = sorted(word_set)
    i=-1
    for word in sorted_words:
        i+=1
        word_to_int_dict[word]=i
        int_to_word_dict[i]=word
    return real_data

crawledposts = process_list_of_jsons(serve_jsons())

with open("../../../../media.csv", 'rb') as f:
    mycsv = csv.reader(f, delimiter = ";")
    mydict = {}
    #goodwords is the set of hashtags that are used by multiple accounts
    goodwords = {}
    totallikes = {}
    totalposts = {}
    avglikes = {}
    avg_author_likes = {}
    assoclist = {}
    for row in mycsv:
        author = row[1]
        tags = row[3]
        likes = row[4]
        tagslist = tags.split(",")
        if author in avg_author_likes:
            (x, y) = avg_author_likes[author]
            avg_author_likes[author] = (x + int(likes), y+1)
        else:
            avg_author_likes[author] = (int(likes), 1)
        if (tags != []):
            for tag in tagslist:
                if (tag in totallikes) and (tag in totalposts):
                    totallikes[tag] += int(likes)
                    totalposts[tag] += 1
                else:
                    totallikes[tag] = int(likes)
                    totalposts[tag] = 1
                if (tag in mydict) and (author not in mydict[tag]) :
                        mydict[tag].append(author)
                        if (tag not in goodwords) and (not tag.isdigit()):
                            goodwords[tag] = 1
                else:
                    mydict[tag] = [author]
                if (tag in goodwords) and (tag in assoclist):
                    assoclist[tag].append((author, likes))
                elif (tag in goodwords) and (tag not in assoclist):
                    assoclist[tag] = [(author,likes)]
            
    for author in crawledposts.keys():
        for likes, tags in crawledposts[author]:
            if author in avg_author_likes:
                (x , y) = avg_author_likes[author]
                avg_author_likes[author] = (x + int(likes), y+1)
            else:
                avg_author_likes[author] = (int(likes), 1)
            if (tags != []):
                for tag in tags:
                    if (tag in totallikes) and (tag in totalposts):
                        totallikes[tag] += int(likes)
                        totalposts[tag] += 1
                    else:
                        totallikes[tag] = int(likes)
                        totalposts[tag] = 1
                if (tag in mydict) and (author not in mydict[tag]) :
                        mydict[tag].append(author)
                        if (tag not in goodwords) and (not tag.isdigit()):
                            goodwords[tag] = 1
                else:
                    mydict[tag] = [author]
                if (tag in goodwords) and (tag in assoclist):
                    assoclist[tag].append((author, likes))
                elif (tag in goodwords) and (tag not in assoclist):
                    assoclist[tag] = [(author,likes)]

    for word in goodwords.keys():
        avglikes[word] = totallikes[word]/totalposts[word]
        
    for poster in avg_author_likes.keys():
        (x, y) = avg_author_likes[poster]
        avg_author_likes[poster] = x/y
    
    for tag in goodwords.keys():
        tmp = 0
        num_post = len(assoclist[tag])
        for (x,y) in assoclist[tag]:
            tmp+=float(y)/float(avg_author_likes[x]+1)
        assoclist[tag] = float(tmp)/float(num_post+1)
        
with open('goodwords.csv', 'w') as csvfile:
    fieldnames = ['goodword', 'avglikes', 'likescore', 'totalposts']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for k in goodwords.keys():
        writer.writerow({'goodword': k, 'avglikes': avglikes[k], 'likescore': assoclist[k], 'totalposts':totalposts[k]})

with open('word_to_int.csv', 'w') as csvfile:
    fieldnames = ['word', 'index']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for k in word_to_int.keys():
        writer.writerow({'word': k, 'index':word_to_int[k]})

with open('inverted_index.csv', 'w') as csvfile:
    fieldnames = ['word', 'numpyarray']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for k in inverted_index.keys():
        writer.writerow({'word': k, 'array':np.array_str(inverted_index[k])})

with open('post_dict.csv', 'w') as csvfile:
    fieldnames = ['post', 'tags']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for k in inverted_index.keys():
        writer.writerow({'post': k, 'tags':post_dict[k]})
