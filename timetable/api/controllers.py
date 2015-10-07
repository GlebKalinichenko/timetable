from timetable.api import api_part
import os

@api_part.route('/')
def index():
    return "Main"

@api_part.route('/hello')
def index2():
    return 'Hello World!'

@api_part.route('/test')
def hello_world2():
    return "TimeTable " + os.environ["ENV_VAR"]