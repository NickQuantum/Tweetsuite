# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 01:01:00 2015

@author: Quantum Solutions
"""
import flask, flask.views
import functools
import tweepy
import json
import uuid
from sys import platform as _platform

sapi = 0
auth = 0

## This method will ensure user is logged in to the application
def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if 'username' in flask.session:
            return method(*args, **kwargs)
        else:
            flask.flash("A login is required to see the page!")
            return flask.redirect(flask.url_for('login'))
    return wrapper

## This method is to connect to Twitter and authenticated
## Sets variables for use in the application
## UUID is created and stored in flask session
## auth - Stores Twitter authorization
## sapi - Stores tweepy connection
def settwitterapi(username):
    flask.session['username'] = username
    uid = uuid.uuid4()
    flask.session['uid'] = uid.urn[9:]
    ## create API Object using Twitter access keys
    ##one time
    consumer_key = "mpIuWJYkQKUvaiS4FPwQpGVr8"
    consumer_secret = "EWOz9A9om3tf85XsF89KbIVC5LUkHEZNhdy2PcHTfOr9tP4jjE"
    access_token = "3080403725-gleW4H38K4tJ69vtUFJDZgBCr2VtqFb3D06Xk7y"
    access_token_secret = "zWxk43qe3c8QlP6Pua2A81UvDTlpe90lqUVC5PxZEzcqg"
    
    global auth
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    global sapi
    sapi = tweepy.API(auth)
    
    print 'twitter account authenticated. stored in variable'
    return
    
def getfilepath():
    if _platform == "linux" or _platform == "linux2":
        filepath = 'static/tweets/'
    elif _platform == "win32":
        filepath = 'static//tweets//'
    
    return filepath
    
    
def getTweets(query):
    flask.session['query'] = query
    max_tweets = 300
    searched_tweets = [status for status in tweepy.Cursor(sapi.search, q=query).items(max_tweets)]
    filepath = getfilepath()
    target = open(filepath + flask.session['uid']+'.txt', 'wb')
    for tweet in searched_tweets:
        tweet_str = json.dumps(tweet._json)
        target.write(tweet_str + "\n")
    
    target.close()