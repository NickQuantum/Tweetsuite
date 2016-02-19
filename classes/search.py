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



from flask import Flask, request, redirect, url_for
from flask import render_template
from flask.views import MethodView
from classes.networkgraph import NetworkGraph


class Search(MethodView):
    def post(self):
        query = request.form['Query']
        tweepy_api = utils.InitializeTweepyAPI()
        
        max_tweets = 300
        
        #Extract tweets using Tweepy Cursor and Write to File   
        searched_tweets = [status for status in tweepy.Cursor(tweepy_api.search, q=query).items(max_tweets)]
        
        #Start Statistics Code (TBD: Move to separate Statistics Class)
        self.createStatistics(searched_tweets);
        
        #End Statistics Code
        
        #Write tweets to file        
        filepath = 'static//tweets//'+ 'tweets_raw.json' 
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
        
        topUserNames = tweet_dataframe['userName'].value_counts()[:5]
        topLocations = tweet_dataframe['userLocation'].value_counts()[:5]
        topRetweets = tweet_dataframe[['text', 'retweetCount']].sort(['retweetCount'], ascending=[0])
        topRetweets = topRetweets.drop_duplicates(cols = 'text', inplace = False)[:5]
        topUrls = tweet_dataframe['urls']
        topHashTags = tweet_dataframe['hashtags']
        
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
            #print key, 'corresponds to', topUrls[key]
            DF = pd.DataFrame(topHashTags[key])
            #print DF
            topHashTagSubsection = topHashTagSubsection.append(DF)
        topHashTagSubsection = topHashTagSubsection['text'].value_counts()[:5]

        #Create TopLocations DataFrame
        topLocations = tweet_dataframe['userLocation']
        topLocations = topLocations.replace('', np.nan, regex=True)
        topLocations = topLocations.dropna()
        topLocations = topLocations.value_counts()[:5]        
        
        #Convert DataFrames to JSON
        topUserNamesJson = topUserNames.to_json(orient = 'index')
        topRetweetsJson = topRetweets.to_json(orient = 'records')
        topUrlJson = topUrlSubsection.to_json(orient = 'index')
        topHashTagJson = topHashTagSubsection.to_json(orient = 'index')
        topLocationsJson = topLocations.to_json(orient = 'index')
        
        #Write JSON to Files
        with open('static//tweets//topUserNames.json', 'w') as outfile:
            json.dump(topUserNamesJson, outfile)
        with open('static//tweets//topRetweets.json', 'w') as outfile:
            json.dump(topRetweetsJson, outfile)
        with open('static//tweets//topUrls.json', 'w') as outfile:
            json.dump(topUrlJson, outfile) 
        with open('static//tweets//topHashTags.json', 'w') as outfile:
            json.dump(topHashTagJson, outfile) 
        with open('static//tweets//topLocations.json', 'w') as outfile:
            json.dump(topLocationsJson, outfile) 