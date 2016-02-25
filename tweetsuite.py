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

tweetsuite = application = Flask(__name__)
tweetsuite.secret_key = "social"                 # needed for sessions

class Mainline(MethodView):
    def get(self):
        session.pop('query', None)              # Reset query value in session
        session.pop('username', None)           # Reset username value in session
        initialize = InitializeTweepyAPI()
        return render_template('index.html')


    
tweetsuite.add_url_rule('/', view_func=Mainline.as_view('index'))
tweetsuite.add_url_rule('/search', view_func=Search.as_view('search'))
tweetsuite.add_url_rule('/result', view_func=Result.as_view('result'))
 
   
if __name__ == '__main__':
    tweetsuite.run(debug=False)