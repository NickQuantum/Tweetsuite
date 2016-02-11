# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 19:32:25 2016

@author: Quantum Solutions
"""

import utils
import json
import networkx as nx
from networkx.readwrite import json_graph

class NetworkGraph():
    
    def __init__(self):    
        self.g = nx.Graph()
        
        self.filepath = 'static//tweets//'+ 'tweets_raw.json' 
        self.tweets_file = open(self.filepath, "r")
        self.tweepy_api = utils.tweepy_api ##utils.InitializeTweepyAPI()    
        
        #Initialize all the Dictionaries and Lists that are needed for the Network 
        #Graph.
        #Initialize all Dictionaries
        
        self.tweet_dict = {} #Dict of all tweet texts with User Id as key
        self.tweet_id_dict = {} #Dict of all tweet Ids with User Id as key
        self.retweet_dict = {} #Dict of all retweet texts with User Id as key
        self.retweet_user_dict = {} #Dict of all Retweet User Ids with User Id as key
        self.mention_tweet_dict = {} #Dict of all mention tweet texts with User Id as key
        self.mention_user_dict = {} #Dict of all Mention User Ids with User Id as key
        self.username_dict = {} #Dict of all User Names with User Id as key
        
        #Initialize all Lists
        self.user_list = [] #List of all User Ids
        self.retweet_user_list = [] #List of all Retweet User Ids
        self.mention_user_listoflists = [] #List of Lists containing all Mention User Ids
        self.mention_user_list = [] #List of all Mention User Ids
        
    
        for line in self.tweets_file:
            try:
                tweet = json.loads(line)
                #hashtags = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
                tweet_id = tweet['id']
                user_id = tweet['user']['id']
                self.tweet_dict[user_id] = tweet['text']
                self.user_list.append(user_id)
                self.tweet_id_dict[user_id] =tweet_id
        
                if 'retweeted_status' in tweet: 
                    #pprint.pprint(tweet)
                    retweet_user_id = tweet['retweeted_status']['user']['id']
                    retweet = tweet['retweeted_status']['text']
                    self.retweet_user_list.append(retweet_user_id)
                    self.retweet_dict[user_id] = retweet
                    self.retweet_user_dict[user_id] = retweet_user_id
                    
                if 'entities' in tweet and len(tweet['entities']['user_mentions']) > 0:
                    mention_user_ids = [mention['id'] for mention in tweet['entities']['user_mentions']]
                    mention_tweet = tweet['text']  
                    self.mention_user_listoflists.append(mention_user_ids)
                    self.mention_tweet_dict[user_id] = mention_tweet
                    self.mention_user_dict[user_id] = mention_user_ids
            except:
                continue
    
    
        #Store all the User Names in a UserName Dict
        for mention_user_ids in self.mention_user_listoflists:
            for mention_user_id in mention_user_ids:
                self.mention_user_list.append(mention_user_id)
                
        #Function used within __init__    
        def get_user_info(user_ids):
            users = self.tweepy_api.lookup_users(user_ids)
            for user in users:
                self.username_dict[user.id] = user.screen_name
            return self.username_dict 

        # Added code to break into chunks of 100 as the api.looup_users has limit of 100 at a time
        # username_dict = get_user_info(user_list + retweet_user_list + mention_user_list)
        complete_user_list = self.user_list + self.retweet_user_list + self.mention_user_list
        chunks=[complete_user_list[x:x+100] for x in xrange(0, len(complete_user_list), 100)]
        for i in range(len(chunks)):
            self.username_dict = get_user_info(chunks[i]) 
            

    def add_node_tw(self, n, weight=None, time=None, source=None):
        if not self.g.has_node(n):
            screen_name = self.username_dict.get(n)
            if n in self.retweet_dict:
                tweet = self.retweet_dict.get(n)
            elif n in self.mention_tweet_dict:
                tweet = self.mention_tweet_dict.get(n)
            else:
                tweet = self.tweet_dict.get(n)
            self.g.add_node(n)
            self.g.node[n]['weight'] = 1
            self.g.node[n]['screen_name'] = screen_name
            self.g.node[n]['tweet'] = tweet            
        else:
            self.g.node[n]['weight']+=1
                
    def add_edge_tw(self,n1,n2, weight=None):
        if not self.g.has_edge(n1,n2):
            self.g.add_edge(n1,n2)
            self.g[n1][n2]['weight']=1
        else:
            self.g[n1][n2]['weight']+=1  
            
    # Create Network Graph by adding Nodes and Edges
    def build_network_graph(self):
        for user_id in self.user_list:
            self.add_node_tw(user_id)
            if user_id in self.retweet_user_dict:
                retweet_user_id = self.retweet_user_dict.get(user_id)           
                self.add_node_tw(retweet_user_id)
                self.add_edge_tw(retweet_user_id,user_id)
            if user_id in self.mention_user_dict:
                for mention_user_id in self.mention_user_dict.get(user_id):
                    self.add_node_tw(mention_user_id)
                    self.add_edge_tw(mention_user_id,user_id)
                    
                    
    def write_networkgraph_json(self):                
        graphjson_filepath = 'static//tweets//'+'sample_graph.json'
        try:
            data = json_graph.node_link_data(self.g)
            ##pprint.pprint(data) 
            with open(graphjson_filepath, 'w') as outfile:
                json.dump(data, outfile)
                print('JSON file Created!')
        except:
            print('JSON FILE Creation FAILED')
            
    