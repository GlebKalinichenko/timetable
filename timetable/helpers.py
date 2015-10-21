# -*- coding: utf-8 -*-
from flask import g
from timetable.models import Faculty

def get_faculties():
    if not hasattr(g, 'faculties'):
        g.faculties = Faculty.objects.all()
    return g.faculties