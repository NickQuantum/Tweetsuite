# -*- coding: utf-8 -*-
"""
Created on Fri Mar 04 07:48:23 2016

@author: srini_000
"""
import utils
import json
import requests
from requests_oauthlib import OAuth1
import collections
from classes.networkgraph import NetworkGraph

class TopInfluencers():
   

    def __init__(self): 
            
        # initialize the network graph code to get the mention usert list and retweet dictionary.
        networkGraph = NetworkGraph()
        self.top_3_influencers= {}
        self.most_common_influencers =[]
        self.iframe_dict ={}  
        self.tweet_id_dict = networkGraph.tweet_id_dict
         # Access values from network graph class
        self.mention_user_list = networkGraph.mention_user_list
        
#        self.filepath = utils.filelocation + 'tweets_raw.json' 
#        self.tweets_file = open(self.filepath, "r")
#        self.tweepy_api = utils.tweepy_api ##utils.InitializeTweepyAPI()  
#        
#        self.tweet_dict = {} #Dict of all tweet texts with User Id as key
#        self.tweet_id_dict = {} #Dict of all tweet Ids with User Id as key
        self.retweet_userid_dict = networkGraph.retweet_user_dict #Dict of all retweet count with user id as key
        
        self.top_3_retweet_dict = {} # dict of top 3 retweet dictionaries with value as url and user id as key
        
        self.influencer_dict = {} # Dict of all influencers (users) with userid as key and url as value
        self.influencer_entities_url = {}
        self.user_entities_url = {}

        self.retweet_max_userid =[]        
        
#        self.user_list = []
#        self.mention_user_listoflists = []
#        self.mention_user_list = []
#        self.user_entities_url_list = []
        
#        for line in self.tweets_file:
#            try:
#                tweet = json.loads(line)
#                tweet_id = tweet['id']
#                user_id = tweet['user']['id']
#                self.tweet_dict[user_id] = tweet['text']
#                self.user_list.append(user_id)
#                self.tweet_id_dict[user_id] =tweet_id
#                
#                self.retweet_userid_dict[user_id] = tweet['retweet_count']
#                
#                if 'entities' in tweet and len(tweet['entities']['user_mentions']) > 0:
#                    mention_user_ids = [mention['id'] for mention in tweet['entities']['user_mentions']]
#                    self.mention_user_listoflists.append(mention_user_ids)
#                     ## The following code gets the urls hosted in the tweet only and not from retweet urls or mention urls
#                if 'entities' in tweet and len(tweet['entities']['urls']) > 0:
#                     self.user_entities_url_list = [reference['url'] for reference in tweet['entities']['urls']]
#                     self.user_entities_url[user_id] = self.user_entities_url_list
#                    
#            except:
#                continue
#        
#        #Store all the User Names in a UserName Dict
#        for mention_user_ids in self.mention_user_listoflists:
#            for mention_user_id in mention_user_ids:
#                self.mention_user_list.append(mention_user_id)
        
        # order the mention user list by mention user id
        #print self.mention_user_list
        self.counter=collections.Counter(self.mention_user_list)
        self.most_common_influencers =self.counter.most_common(5)
          
        self.top_3_influencers= dict( self.most_common_influencers)
       
        

        # Retweet count logic        
        def keyfunction(k):
            return self.retweet_userid_dict[k]
            
        # create the top 3 influencers by sorting the top 3 from mention user list
        for key in sorted(self.retweet_userid_dict, key=keyfunction, reverse=True)[:3]:
           #print "%s: %i" % (key, influencer_dict[key])
           #url_dict = self.user_entities_url.get(key)
           value =''
           #if url_dict is not  None:
           #      value = url_dict
           self.top_3_retweet_dict[key] = value
          
        
        
    def build_influencer_iframe(self): 
        try:
            ## make a REST aPI call 
            ## https://api.twitter.com/1.1/statuses/oembed.json?maxwidth=250&hide_media=1&hide_thread=1&omit_script=1&align=left&id=638229069251899392
            ## get the user id from the above dictionary and make a call  
            ## store the results in html
            ## add oauth
            ##headers = {'consumer_key':'5zvyqirbbnbPxUX67ixXBwQ5G','consumer_secret':'8iGil6zWJvK7qjGj0z7xguSvaiIbZtpH0Z3UumAVetv88e9xbX','access_token':'2995170696-z5tNgtrnhR5zc5tT4sB6knKBTrCKHehOljhs1l2','access_token_secret':'wOcuYhfpvwxFZ6TmNvyPb9fPpEnH1fvfApiEZFnFGUuJk'}
            auth = OAuth1('5zvyqirbbnbPxUX67ixXBwQ5G','8iGil6zWJvK7qjGj0z7xguSvaiIbZtpH0Z3UumAVetv88e9xbX','2995170696-z5tNgtrnhR5zc5tT4sB6knKBTrCKHehOljhs1l2','wOcuYhfpvwxFZ6TmNvyPb9fPpEnH1fvfApiEZFnFGUuJk')
            ##iframe_dict ={userid1: {'url':1,'html':2},userid2: {'url':3,'html':4}, userid3: {'url':5,'html':6}}
           
            
            for key,value in self.top_3_retweet_dict.iteritems():
                
                tweetid = self.tweet_id_dict.get(key)
                if tweetid > 0: 
                    payload ={}
                    payload['id'] = tweetid
                    
                    r = requests.get('https://api.twitter.com/1.1/statuses/oembed.json?maxwidth=250&hide_media=1&hide_thread=1&omit_script=1&align=left',params =payload,auth =auth)
                    
                    htmlcontent = r.json()
                    self.iframe_dict[key] ={}
                    
                    
                    internal_dict = {'html':1,'url':2}
                    internal_dict['html'] = htmlcontent['html']
                   
                    internal_dict['url'] = self.user_entities_url.get(key)
                    ##iframe_list.append(htmlcontent['html'])
                    self.iframe_dict[key] = internal_dict
                
                ##print htmlcontent['html']
        except Exception , err:
            print('twitter api call FAILED')
            print Exception, err.message
            
    def build_influencer_iframe2(self): 
        try:
            ## make a REST aPI call 
            ## https://api.twitter.com/1.1/statuses/oembed.json?maxwidth=250&hide_media=1&hide_thread=1&omit_script=1&align=left&id=638229069251899392
            ## get the user id from the above dictionary and make a call  
            ## store the results in html
            ## add oauth
            ##headers = {'consumer_key':'5zvyqirbbnbPxUX67ixXBwQ5G','consumer_secret':'8iGil6zWJvK7qjGj0z7xguSvaiIbZtpH0Z3UumAVetv88e9xbX','access_token':'2995170696-z5tNgtrnhR5zc5tT4sB6knKBTrCKHehOljhs1l2','access_token_secret':'wOcuYhfpvwxFZ6TmNvyPb9fPpEnH1fvfApiEZFnFGUuJk'}
            auth = OAuth1('5zvyqirbbnbPxUX67ixXBwQ5G','8iGil6zWJvK7qjGj0z7xguSvaiIbZtpH0Z3UumAVetv88e9xbX','2995170696-z5tNgtrnhR5zc5tT4sB6knKBTrCKHehOljhs1l2','wOcuYhfpvwxFZ6TmNvyPb9fPpEnH1fvfApiEZFnFGUuJk')
            ##iframe_dict ={userid1: {'url':1,'html':2},userid2: {'url':3,'html':4}, userid3: {'url':5,'html':6}}
            self.userprofile = {}
            self.useridstr = ""
            for key,value in self.top_3_influencers.iteritems():
                if self.useridstr == "" :
                    self.useridstr = self.useridstr + str(key)
                else:
                    self.useridstr= self.useridstr + "," + str(key)
                 
                   
            
            r = requests.get('https://api.twitter.com/1.1/users/lookup.json?user_id=' + self.useridstr,auth =auth)
          
            self.userprofile = r.json()
            ##print self.userprofile
            ## Create the data that need to be passed to the show_influencertable
            
        except Exception , err:
            print('twitter api call 2 FAILED')
            print Exception, err.message
          
    def write_influencer_dict(self):
        ##print iframe_dict
        filepathjson = 'static//tweets//'+ 'influencer_urls.json'  ##'/tmp/tweetgraph.json' 
            
        try:
                  
             with open(filepathjson, 'w') as outfile:
             
               json.dump(self.iframe_dict,outfile)
                 
               
           
                          
        except Exception,err:
            print('JSON FILE Creation FAILED')
            print Exception, err  
            
    def write_influencer_dict2(self):
        ##print iframe_dict
        filepathjson = 'static//tweets//'+ 'influencer_users.json'  ##'/tmp/tweetgraph.json' 
            
        try:
             
             
             with open(filepathjson, 'w') as outfile:
             
               json.dump(self.userprofile,outfile)
              
               
           
                          
        except Exception,err:
            print('JSON FILE Creation FAILED')
            print Exception, err    