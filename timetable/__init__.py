from flask import Flask
from timetable.api import api_part
import os

app = Flask(__name__)
app.config['SERVER_NAME'] = os.environ["SERVER_NAME"] # 'localhost:5000'

import timetable.controllers
import timetable.api.controllers

app.register_blueprint(api_part, url_prefix='/api') # subdomain='api'