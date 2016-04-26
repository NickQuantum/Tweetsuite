# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 00:45:30 2016

@author: Quantum Solutions
"""
import tweepy
import flask
import uuid

tweepy_api = 0      # declare global variable to store tweepy api
filelocation = None   # declare global variable to store file prefix
jsfilelocation = None # declare global variable to store js file prefix

def Init_SessionVar():
    try:
        valid = flask.session['uid']
        fileuid = valid
    except:
        uid = uuid.uuid4()                          # Set unique session id
        flask.session['uid'] = fileuid = uid.urn[9:]

    global filelocation
    filelocation = "static//tweets//" + fileuid + "_"
    global jsfilelocation
    jsfilelocation = "static/tweets/" + fileuid + "_"
    return

def InitializeTweepyAPI():
    session_username = 0
    try:
        session_username = flask.session['username']
    except:
        session_username = None

    if session_username is None:
        flask.session['username'] = "demo"            # Set username in session
        Init_SessionVar()

        consumer_key = "6XhZ7RX6saKTPEqHfGMVmLOzU"
        consumer_secret = "iNVdx2FQMInmdlwqMDMQKn6FkwXAN11QbuPhJ27mOlEDIkL5E2"
        access_token = "2982175576-8vtYkFFQQ6A2w1UdzfhUjRQTEhBZfPyXMIfSbSK"
        access_token_secret = "wvo4uBMdK9E9gnod4glyrGk0CsAX43dsnQ5LuNDlfoY4l"
        
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        global tweepy_api        
        tweepy_api = tweepy.API(auth)

    return tweepy_api
    
    