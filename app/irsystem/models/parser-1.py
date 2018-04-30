import csv
import os
import json
import numpy as np
import re
import math

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

    for json_name in lst_of_jsons:
        with open(basedir+json_name) as f:
            data = json.load(f)
        posts = data['posts']
        try :
            for post in posts:
                tags = post['tags']
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
