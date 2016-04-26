# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 22:35:04 2016

@author: Quantum Solutions
"""

import utils
import json
import tweepy
import pandas as pd
import numpy as np
import nltk
import re



from flask import Flask, request, redirect, url_for, session
from flask import render_template
from flask.views import MethodView
from classes.networkgraph import NetworkGraph


class Search(MethodView):
    def get(self):
        return redirect(url_for('index'))

    
    def post(self):
        query = request.form['Query']
        try:
            session['query'] = query
        except:
            print "loading query to session failed"
        tweepy_api = utils.tweepy_api
        
        max_tweets = 500
        
        #Extract tweets using Tweepy Cursor and Write to File   
        searched_tweets = [status for status in tweepy.Cursor(tweepy_api.search, q=query).items(max_tweets)]
        #Start Statistics Code (TBD: Move to separate Statistics Class)
        self.createStatistics(searched_tweets);
        
        #End Statistics Code
        
        #Write tweets to file        
        filepath = utils.filelocation + 'tweets_raw.json' 
        target = open(filepath, 'w')
        
        for tweet in searched_tweets:
            tweet_str = json.dumps(tweet._json)
            target.write(tweet_str + "\n")
        
        target.close()
        
        #Build and Write Network Graph JSon 
        networkGraph = NetworkGraph()
        networkGraph.build_network_graph()
        networkGraph.write_networkgraph_json()
        
        
        return redirect(url_for('result'))
        
   
    def processTweet(self, tweet):
        # process the tweets
    
        #Convert to lower case
        tweet = tweet.lower()
        #Convert www.* or https?://* to URL
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
        #Remove additional white spaces
        tweet = re.sub('[\s]+', ' ', tweet)
        #Replace #word with word
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        #trim
        tweet = tweet.strip('\'"')
        return tweet
    

    def createStatistics(self, tweets):
        #Build Tweets Dataframe
        searched_tweets = tweets
        tweet_dataframe = pd.DataFrame()
        tweet_dataframe['userName'] = [tweet.user.screen_name for tweet in searched_tweets]
        tweet_dataframe['text'] = [tweet.text for tweet in searched_tweets]
        tweet_dataframe['retweetCount'] = [tweet.retweet_count for tweet in searched_tweets]
        tweet_dataframe['userLocation'] = [tweet.user.location for tweet in searched_tweets]  
        tweet_dataframe['urls'] = [tweet.entities["urls"] for tweet in searched_tweets]
        tweet_dataframe['hashtags'] = [tweet.entities["hashtags"] for tweet in searched_tweets]        
        tweet_dataframe['mentions'] = [tweet.entities["user_mentions"] for tweet in searched_tweets]
        tweet_dataframe['language'] = [tweet.user.lang for tweet in searched_tweets]        
        
        topUserNames = tweet_dataframe['userName'].value_counts()[:5]
        topLocations = tweet_dataframe['userLocation'].value_counts()[:5]
        topRetweets = tweet_dataframe[['text', 'retweetCount']].sort(['retweetCount'], ascending=[0])
        topRetweets = topRetweets.drop_duplicates(cols = 'text', inplace = False)[:5]
        topUrls = tweet_dataframe['urls']
        topHashTags = tweet_dataframe['hashtags']
        topMentions = tweet_dataframe['mentions']
        topLanguages = tweet_dataframe['language'].value_counts()[:5]
        
        #Create URL SubSection DataFrame
        topUrlSubsection = pd.DataFrame()
        topUrls = topUrls.to_dict()
        for key, value in topUrls.iteritems():
            DF = pd.DataFrame(topUrls[key])
            topUrlSubsection = topUrlSubsection.append(DF)
        topUrlSubsection = topUrlSubsection['display_url'].value_counts()[:5]
        
        #Create HashTag Subsection Dataframe
        topHashTagSubsection = pd.DataFrame()
        topHashTags = topHashTags.to_dict()
        for key, value in topHashTags.iteritems():
            DF = pd.DataFrame(topHashTags[key])
            topHashTagSubsection = topHashTagSubsection.append(DF)
        topHashTagSubsection = topHashTagSubsection['text'].value_counts()[:5]
        
        #Create Mentions Subsection Dataframe
        topMentionsSubsection = pd.DataFrame()
        topMentions = topMentions.to_dict()
        for key, value in topMentions.iteritems():
            DF = pd.DataFrame(topMentions[key])
            topMentionsSubsection = topMentionsSubsection.append(DF)
        topMentionsSubsection = topMentionsSubsection['screen_name'].value_counts()[:5]

        #Create TopLocations DataFrame
        topLocations = tweet_dataframe['userLocation']
        topLocations = topLocations.replace('', np.nan, regex=True)
        topLocations = topLocations.dropna()
        topLocations = topLocations.value_counts()[:5]   
        
        #Get Top Words from Tweets
        topWords = tweet_dataframe['text'].values.tolist()
        #topWords = topWords.values.tolist()
        topWordsList = []
        for sentence in topWords:
            sentence = self.processTweet(sentence)
            topWordsList = topWordsList + sentence.split()
        #Vocab = set(topWordsList)
        long_words = [w for w in topWordsList if len(w) > 6]
        
        fdist = nltk.FreqDist(long_words)
        topWords = fdist.most_common(5)
        topWords = json.dumps(topWords)
        
        #Convert DataFrames to JSON
        topUserNamesJson = topUserNames.to_json(orient = 'index')
        topRetweetsJson = topRetweets.to_json(orient = 'records')
        topUrlJson = topUrlSubsection.to_json(orient = 'index')
        topHashTagJson = topHashTagSubsection.to_json(orient = 'index')
        topLocationsJson = topLocations.to_json(orient = 'index')
        topMentionsJson = topMentionsSubsection.to_json(orient = 'index')
        topLanguagesJson = topLanguages.to_json(orient = 'index')        
        
        #Write JSON to Files
        print(utils.filelocation)
        with open(utils.filelocation + 'topUserNames.json', 'w') as outfile:
            json.dump(topUserNamesJson, outfile)
        with open(utils.filelocation + 'topRetweets.json', 'w') as outfile:
            json.dump(topRetweetsJson, outfile)
        with open(utils.filelocation + 'topUrls.json', 'w') as outfile:
            json.dump(topUrlJson, outfile) 
        with open(utils.filelocation + 'topHashTags.json', 'w') as outfile:
            json.dump(topHashTagJson, outfile) 
        with open(utils.filelocation + 'topLocations.json', 'w') as outfile:
            json.dump(topLocationsJson, outfile) 
        with open(utils.filelocation + 'topMentions.json', 'w') as outfile:
            json.dump(topMentionsJson, outfile) 
        with open(utils.filelocation + 'topLanguages.json', 'w') as outfile:
            json.dump(topLanguagesJson, outfile) 
        with open(utils.filelocation + 'topWords.json', 'w') as outfile:
            json.dump(topWords, outfile) 