# -*- coding: utf-8 -*-
from timetable import app
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, send_from_directory
from models import Faculty     
import os

def get_faculties():
    if not hasattr(g, 'faculties'):
        g.faculties = Faculty.objects.all()
    return g.faculties

@app.route('/')
def index():
    #return 'Hello World!'
    return render_template('index.html', faculties=get_faculties())

@app.route('/mobile')
def mobile():
    data={
        "page": "mobile",
        "title": "Mobile",
        "page_name": "Mobile App"
    }
    return render_template('_main.html', data=data)   
    
@app.route('/help')
def help():
    data={
        "page": "help",
        "title": int("Help"),
        "page_name": "Help"
        
    }
    return render_template('_main.html', data=data)   
    
@app.route('/about')
def about():
    data={
        "page": "about",
        "title": "About",
        "page_name": "About",
    }
    return render_template('_main.html', data=data)   
    
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'config_date.ico', mimetype='image/vnd.microsoft.icon')


@app.errorhandler(404)
def not_found(e):
    data={
        "page": "error",
        "title": str(e),
        "page_name": "Sorry, but the page is not found",
        "error": """You step in the stream, </br>
                    but the water has moved on.</br>
                    This page is not here."""
    }
    return render_template('_main.html', data=data), 404
    
@app.errorhandler(500)
def not_found(e):
    data={
        "page": "error",
        "title": "500: Internal Server Error",
        "page_name": "Internal Server Error",
        "error": """The Web site you seek </br>
                    cannot be located but </br>
                    endless others exist."""
    }
    return render_template('_main.html', data=data), 500