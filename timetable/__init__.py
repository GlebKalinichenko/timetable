from flask import Flask
from timetable.api import api_part

app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:5000'

import timetable.controllers
import timetable.api.controllers

app.register_blueprint(api_part, subdomain='api', url_prefix='/v1') # /api