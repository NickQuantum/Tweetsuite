# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 12:50:34 2016

@author: Quantum Solutions
"""
#import flask
from flask import Flask, request, redirect, url_for, render_template, session
from flask.views import MethodView
from classes.utils import settwitterapi, auth, sapi, getfilepath, getTweets

#Declare the application
tweetsuite = application = Flask(__name__)
tweetsuite.secret_key = "social"

class Mainline(MethodView):
    def get(self):
        self.initialize_instance()                   # call initialize_instance local method
        return render_template('index.html')
        
    def initialize_instance(self):
        session.pop('query', None)              # Reset query value in session
        session.pop('username', None)           # Reset username value in session
        username = "demo"
        settwitterapi(username)
        return  
      
        
class Search(MethodView):
    def post(self):
        query = request.form['Query']
        getTweets(query)        
        return redirect(url_for('result'))
        
class Result(MethodView):
    def get(self):
        return render_template('show_results.html',filepath = session['uid'])    
    
   
        
tweetsuite.add_url_rule('/', view_func=Mainline.as_view('index'))
tweetsuite.add_url_rule('/search', view_func=Search.as_view('search'))
tweetsuite.add_url_rule('/result', view_func=Result.as_view('result'))
 
   
if __name__ == '__main__':
    tweetsuite.run(debug=True)