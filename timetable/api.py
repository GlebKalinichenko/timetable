from timetable import app
import os

@app.route('/hello')
def index2():
    return 'Hello World!'

@app.route('/test')
def hello_world2():
    return "TimeTable " + os.environ["ENV_VAR"]