# -*- coding: utf-8 -*-
from timetable.schedule import schedule_part
from timetable.models import Faculty
import os
import json
from flask import Response, request, g

def get_faculties():
    if not hasattr(g, 'faculties'):
        g.faculties = Faculty.objects.all()
    return g.faculties

@schedule_part.route('/')
def index():
    return "Main"

@schedule_part.route('/faculties/', methods=['GET', 'POST'])
@schedule_part.route('/faculty/<faculty>', methods=['GET', 'POST'])
def faculty(faculty='all'):
    fs = []
    if request.method == 'GET':
        
        if faculty == 'all':
            fs = map(lambda i: i.abbr, get_faculties())
            
        else:
            pass
    
        return str(faculty) + " " + "\r\n".join(fs)
    else:
        return "Post"
    