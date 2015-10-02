from flask import Flask

app = Flask(__name__)

import timetable.views
import timetable.api