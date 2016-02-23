# -*- coding: utf-8 -*-
"""
Created on Tue Feb 02 22:40:57 2016

@author: Quantum Solutions
"""

import json

from flask import Flask, request, redirect, url_for
from flask import render_template
from flask.views import MethodView
import utils

class Result(MethodView):
    def get(self):
        
        #Parse raw tweets file and create list of tweets for Tweet Table
        filepath = utils.filelocation + 'tweets_raw.json'
        tweets_data = []
        tweets_file = open(filepath, "r")
        for line in tweets_file:
            try:
                tweet = json.loads(line)
                hashtags = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
                #print(hashtags)
                tweets_data.append([tweet["text"],tweet["user"]["screen_name"],
                                         hashtags])
                #pprint.pprint(tweets_data)
                        
            except:
                print('error found')
                continue
        
        #Write list of tweets for Tweet Table into a File
        filepath = utils.filelocation + 'sample_tweets.txt'
        target = open(filepath, 'w')
        
        for tweet in tweets_data:
            tweet_str = json.dumps(tweet)
            target.write(tweet_str + "\n")
        
        target.close()
        
        
        
        
        return render_template('show_results.html', tweets = tweets_data)   