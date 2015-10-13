from timetable.api import api_part
import os
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

@api_part.route('/hello')
def index2():
    return Response('{"hello": "Hello World!"}', content_type='application/json; charset=utf-8')

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
    