# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 00:45:30 2016

@author: Quantum Solutions
"""
import tweepy

def InitializeTweepyAPI():
    
    consumer_key = "6XhZ7RX6saKTPEqHfGMVmLOzU"
    consumer_secret = "iNVdx2FQMInmdlwqMDMQKn6FkwXAN11QbuPhJ27mOlEDIkL5E2"
    access_token = "2982175576-8vtYkFFQQ6A2w1UdzfhUjRQTEhBZfPyXMIfSbSK"
    access_token_secret = "wvo4uBMdK9E9gnod4glyrGk0CsAX43dsnQ5LuNDlfoY4l"
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    tweepy_api = tweepy.API(auth)
    return tweepy_api
    
    