# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 12:50:34 2016

@author: Quantum Solutions
"""


from flask import Flask, request, redirect, url_for
from flask import render_template
from flask.views import MethodView

tweetsuite = Flask(__name__)

class HelloWorld(MethodView):
    def get(self):
        return render_template('index.html')
        
class Search(MethodView):
    def post(self):
        query = request.form['Query']
        return redirect(url_for('result'))
        
class Result(MethodView):
    def get(self):
        return render_template('show_results.html')    
    
   
        
tweetsuite.add_url_rule('/', view_func=HelloWorld.as_view('arbitrary'))
tweetsuite.add_url_rule('/search', view_func=Search.as_view('search'))
tweetsuite.add_url_rule('/result', view_func=Result.as_view('result'))
 
   
if __name__ == '__main__':
    tweetsuite.run(debug=True)