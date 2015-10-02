from timetable import app
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
     
import os

@app.route('/')
def index():
    #return 'Hello World!'
    return render_template('index.html')

@app.route('/timetable')
def hello_world():
    return "TimeTable " + os.environ["ENV_VAR"]