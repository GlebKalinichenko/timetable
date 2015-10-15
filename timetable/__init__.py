# -*- coding: utf-8 -*-
from flask import Flask, g
from flask.ext.mongoengine import MongoEngine
from timetable.api import api_part
from timetable.schedule import schedule_part
import os

app = Flask(__name__)

app.config['MONGODB_DB'] = os.environ["MONGODB_DB"]
app.config['MONGODB_HOST'] = os.environ["MONGODB_HOST"]
app.config['MONGODB_PORT'] = os.environ["MONGODB_PORT"]
app.config['MONGODB_USERNAME'] = os.environ["MONGODB_USERNAME"]
app.config['MONGODB_PASSWORD'] = os.environ["MONGODB_PASSWORD"]

app.config['SERVER_NAME'] = os.environ["SERVER_NAME"] # 'localhost:5000'

db = MongoEngine(app)

import timetable.controllers
import timetable.api.controllers
import timetable.schedule.controllers


app.register_blueprint(api_part, url_prefix='/api') # subdomain='api'
app.register_blueprint(schedule_part, url_prefix='/schedule') # subdomain='schedule'
