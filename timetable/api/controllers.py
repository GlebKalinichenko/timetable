# -*- coding: utf-8 -*-
from timetable.api import api_part
from timetable.models import Faculty
import os
import json
from flask import Response, request
from functools import wraps

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

@api_part.route('/help')
@returns_json
def hello_world2():
    return "{\"key\": \"TimeTable " + os.environ["ENV_VAR"] + "\"}"

#@api_part.route('/method/')    
@api_part.route('/method/', methods=['GET', 'POST'], defaults={'api_method': "TEst"})
@api_part.route('/method/<api_method>', methods=['GET', 'POST'])
@returns_json
def method(api_method=None):
    if request.method == 'GET':
        return "{\"key\": \"" + str(api_method) + "\"}"
    else:
        return "Post"
    