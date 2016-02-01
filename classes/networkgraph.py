# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 19:32:25 2016

@author: Quantum Solutions
"""

import networkx as nx
from networkx.readwrite import json_graph

    g = nx.Graph()
    filepath = 'static//tweets//'+ 'tweets_raw.json' 
    tweets_file = open(filepath, "r")    
    
    #Initialize all the Dictionaries and Lists that are needed for the Network 
    #Graph.
    #Initialize all Dictionaries
    
    tweet_dict = {} #Dict of all tweet texts with User Id as key
    tweet_id_dict = {} #Dict of all tweet Ids with User Id as key
    retweet_dict = {} #Dict of all retweet texts with User Id as key
    retweet_user_dict = {} #Dict of all Retweet User Ids with User Id as key
    mention_tweet_dict = {} #Dict of all mention tweet texts with User Id as key
    mention_user_dict = {} #Dict of all Mention User Ids with User Id as key
    
    #Initialize all Lists
    user_list = [] #List of all User Ids
    retweet_user_list = [] #List of all Retweet User Ids
    mention_user_list = [] #List of all Mention User Ids
        
    
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            #hashtags = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
            tweet_id = tweet['id']
            user_id = tweet['user']['id']
            tweet_dict[user_id] = tweet['text']
            user_list.append(user_id)
            tweet_id_dict[user_id] =tweet_id
    
            if 'retweeted_status' in tweet: 
                #pprint.pprint(tweet)
                retweet_user_id = tweet['retweeted_status']['user']['id']
                retweet = tweet['retweeted_status']['text']
                retweet_user_list.append(retweet_user_id)
                retweet_dict[user_id] = retweet
                retweet_user_dict[user_id] = retweet_user_id
                
            if 'entities' in tweet and len(tweet['entities']['user_mentions']) > 0:
                mention_user_ids = [mention['id'] for mention in tweet['entities']['user_mentions']]
                mention_tweet = tweet['text']  
                mention_user_list.append(mention_user_ids)
                mention_tweet_dict[user_id] = mention_tweet
                mention_user_dict[user_id] = mention_user_ids
        except:
            continue
    