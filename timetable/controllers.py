# -*- coding: utf-8 -*-
from timetable import app
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
     
import os

@app.route('/')
def index():
    #return 'Hello World!'
    return render_template('index.html')

@app.route('/mobile')
def mobile():
    return 'mobileApp'    
    
@app.route('/help')
def help():
    return 'help'
    
@app.route('/about')
def about():
    return "about"
    
