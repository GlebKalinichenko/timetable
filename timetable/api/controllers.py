# -*- coding: utf-8 -*-
from timetable.api import api_part
from timetable.models import Faculty
import os
import json
import engine
from flask import Response, request
from functools import wraps

CURRENT_API_V = "0.1"
APIS = {
    "0.1": engine.v0_1,
    "0.2": engine.v0_2,
}

def returns_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        r = f(*args, **kwargs)
        return Response(r, content_type='application/json; charset=utf-8')
    return decorated_function

@api_part.route('/')
def index():
    return "Main"

@api_part.route('/json')
@returns_json
def test_json():
    cs = {}
    knt = Faculty.objects(abbr="cs").first()
    cs["title"] = knt.title
    cs["abbr"] = knt.abbr
    cs["description"] = knt.description
    cs["groups"] = []
    for g in knt.groups:
        cs["groups"].append({"title": g.title, "abbr": g.abbr, "description": g.description}) 
    return json.dumps(cs, ensure_ascii=False, indent=4)
    
@api_part.route('/hello/<m>.<a>')
def index2(m, a):
    return '{' + m + " " + a + '}'#Response('{"hello": "Hello World!"}', content_type='application/json; charset=utf-8')

@api_part.route('/<path:invalid_path>')
@returns_json
def other(invalid_path):
    #http://stackoverflow.com/questions/19660013/flask-per-blueprint-error-pages
    return engine.error(9) #invalid_path

@api_part.route('/<entity>.<method>', methods=['GET', 'POST'])
@returns_json
def method(entity=None, method=None):
    # request.query_string
    # http://flask.pocoo.org/docs/0.10/api/#response-objects

    ver = request.args.get("v", CURRENT_API_V)

    if not (ver in APIS):
        return engine.error(1)
    
    tapi = APIS.get(ver, APIS[CURRENT_API_V])()
  
    if request.method == 'GET':
        return tapi.execute(entity, method, request.args)
    elif request.method == 'POST':
        return engine.error(2)
