# -*- coding: utf-8 -*-
from timetable.schedule import schedule_part
from timetable.models import Faculty, Lecturer, Group, Weekday
import os
import json
from flask import Response, request, g, render_template

def get_faculties():
    if not hasattr(g, 'faculties'):
        g.faculties = Faculty.objects.all()
    return g.faculties

@schedule_part.route('/')
def index():
    return "Main schedule" #render_template('no-sidebar.html')

@schedule_part.route('/faculties/', methods=['GET', 'POST'])
@schedule_part.route('/faculty/<faculty>', methods=['GET', 'POST'])
def faculty(faculty='all'):
    fs = []
    if request.method == 'GET':
        
        if faculty == 'all':
            fs = map(lambda i: i.abbr, get_faculties())
            
        else:
            pass
    
        return str(faculty) + " " + "<br />".join(fs)
    else:
        return "Post"
        
@schedule_part.route('/lecturers/', methods=['GET', 'POST'])
@schedule_part.route('/lecturer/<lecturer>', methods=['GET', 'POST'])
def lecturer(lecturer='all'):
    lect = []
    if request.method == 'GET':
        
        if lecturer == 'all':
            lect = map(lambda i: i.name, Lecturer.objects.all())
            
        else:
            lect = map(lambda i: i.name, Lecturer.objects(id=lecturer).all())
    
        return str(lecturer) + " " + "<br />".join(lect)
    else:
        return "Post"

   
@schedule_part.route('/groups/', methods=['GET', 'POST'])
@schedule_part.route('/group/<group>', methods=['GET', 'POST'])
def group(group='all'):
    res = ""
    if request.method == 'GET':
        if group == 'all':
            res = 'all'           
        else:
            gr = Group.objects(abbr=group).first()
            res = gr.title + "<br />"
            lessons = gr.lessons
            res = res + u"Понидельник:" + "<br />"
            l = filter(lambda i: i.weekday == Weekday.MONDAY, lessons)
            res = res + u"<br />".join(map(lambda i: i.title + u", " + i.lecturer.name + u", " + i.room, sorted(l, key=lambda i: i.item_number)))
    return res            
                