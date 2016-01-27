# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 22:35:04 2016

@author: Quantum Solutions
"""

from flask import Flask, request, redirect, url_for
from flask import render_template
from flask.views import MethodView

class Search(MethodView):
    def post(self):
        query = request.form['Query']
        return redirect(url_for('result'))