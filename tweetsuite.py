# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 12:50:34 2016

@author: Quantum Solutions
"""



from flask import Flask, request, redirect, url_for
from flask import render_template, session
from flask.views import MethodView
from classes.search import Search
from classes.result import Result
from classes.utils import InitializeTweepyAPI

import tweepy
import classes.utils

tweetsuite = application = Flask(__name__)
application.secret_key = "social"                 # needed for sessions


consumer_key = "mpIuWJYkQKUvaiS4FPwQpGVr8"
consumer_secret = "EWOz9A9om3tf85XsF89KbIVC5LUkHEZNhdy2PcHTfOr9tP4jjE"
callback_url = 'http://localhost:5000/verify'
#callback_url = 'http://tweetsuite-dev.us-east-1.elasticbeanstalk.com/verify'

class Mainline(MethodView):
    def get(self):
        #initialize = InitializeTweepyAPI()
        classes.utils.Init_SessionVar()
        try:
            valid = session['access_token']
            return render_template('index.html')
        except:
            return redirect(url_for('login'))

class Login(MethodView):
    def get(self):
        redirect_url = ""
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret,callback_url)
        try:
            #get the request tokens
            redirect_url= auth.get_authorization_url()
            session['request_token']= auth.request_token
        except:
            print 'Error! Failed to get request token'
        #this is twitter's url for authentication
        htmlstring= "<div style='width:200px;margin-top:200px;margin-left:auto;margin-right:auto'>"
        htmlstring = htmlstring + "<a id='redirecturl' href='"+redirect_url+ "'><img src='https://g.twimg.com/dev/sites/default/files/images_documentation/sign-in-with-twitter-gray.png' alt='Sign in with Twitter' title='Sign in with Twitter'></a>"
        return htmlstring

class Verify(MethodView):
    def get(self):
        try:
            request.args['denied']              # When twitter authorization fails
            return redirect(url_for('login'))
        except:
            pass
        #get the verifier key from the request url
        verifier= request.args['oauth_verifier']
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        token = session['request_token']
        del session['request_token']

        auth.request_token = token
        try:
                access_token = auth.get_access_token(verifier)
                session['access_token'] = access_token
        except tweepy.TweepError:
                print 'Error! Failed to get access token.'
        classes.utils.tweepy_api = tweepy.API(auth)
        print " all session --> " , session
        try:
            user = classes.utils.tweepy_api.me()
            session['username'] = user.screen_name
        except:
            print "get user screen_name failed"

        return redirect(url_for('search'))

class Logout(MethodView):
    def get(self):
        session.pop('query', None)              # Reset query value in session
        session.pop('username', None)           # Reset username value in session
        session.pop('access_token', None)       # Reset access_token in session
        session.pop('uid', None)                # Reset access_token in session
        session.pop('access_token', None)       # Reset access_token in session
        print "session AFTER LOGOUT --> " , session
        return redirect(url_for('login'))


tweetsuite.add_url_rule('/', view_func=Mainline.as_view('index'))
tweetsuite.add_url_rule('/login', view_func=Login.as_view('login'))
tweetsuite.add_url_rule('/verify', view_func=Verify.as_view('verify'))
tweetsuite.add_url_rule('/logout', view_func=Logout.as_view('logout'))
tweetsuite.add_url_rule('/search', view_func=Search.as_view('search'))
tweetsuite.add_url_rule('/result', view_func=Result.as_view('result'))
 
   
if __name__ == '__main__':
    tweetsuite.run(debug=False)