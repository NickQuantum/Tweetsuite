# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 22:35:04 2016

@author: Quantum Solutions
"""

import utils
import json
import tweepy



from flask import Flask, request, redirect, url_for
from flask import render_template
from flask.views import MethodView
from classes.networkgraph import NetworkGraph


class Search(MethodView):
    def post(self):
        query = request.form['Query']
        tweepy_api = utils.InitializeTweepyAPI()
        print tweepy_api
        max_tweets = 300
        
        #Extract tweets using Tweepy Cursor and Write to File   
        searched_tweets = [status for status in tweepy.Cursor(tweepy_api.search, q=query).items(max_tweets)]
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