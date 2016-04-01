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
import ast

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
        
         #Parse raw influencer users file and create list of influencer users
        filepath = 'static//tweets//' + 'influencer_users.json'
        influencer_user_data = []
        influencer_user_file = open(filepath, "r")
        
        for line in influencer_user_file:
            try:
                influencer_user = json.loads(line)
               
                        
            except Exception,err:
                print('error found2')
                print Exception, err
                continue
        
       
        for i in range(len(influencer_user)):
            influencer_user_data.append([influencer_user[i]["screen_name"],influencer_user[i]["followers_count"],influencer_user[i]["description"],influencer_user[i]["location"],influencer_user[i]["profile_image_url_https"],influencer_user[i]["statuses_count"],influencer_user[i]["name"],influencer_user[i]["friends_count"],influencer_user[i]["favourites_count"]])
        
        #Write list of influencer users into a file
        filepath = 'static//tweets//' + 'influencer_users.txt'
        target = open(filepath, 'w')
        
        for influencer_user in influencer_user_data:
            influencer_user_str = json.dumps(influencer_user)
            target.write(influencer_user_str + "\n")
        
        target.close()
            
       
        #Parse raw influencers file and create list of influencers for Influencers Table
        filepath = 'static//tweets//' +'influencer_urls.json'
        influencer_data = []
        html_file = open(filepath, "r")
        for line in html_file:
             
            try:
                html  = json.loads(line)
                
                for key in html :
                    userid = key
                    influencer_data.append([html[userid]['html'],html[userid]['url']])
                #pprint.pprint(tweets_data)
                #print influencer_data        
            except:
                print('error found')
                continue
        
        #Write list of tweets for Tweet Table into a File
        filepath = 'static//tweets//'+ 'sample_html.txt'
        target = open(filepath, 'w')
        
        for html in influencer_data:
            html_str = json.dumps(html)
            target.write(html_str + "\n")
        
        target.close()
                
        return render_template('show_results.html', tweets = tweets_data, html =influencer_data, users = influencer_user_data)   