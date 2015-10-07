from timetable.api import api_part
import os
from flask import Response
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

@api_part.route('/test')
@returns_json
def hello_world2():
    return "{\"key\": \"TimeTable " + os.environ["ENV_VAR"] + "\"}"
    