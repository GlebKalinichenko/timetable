# -*- coding: utf-8 -*-
from timetable.models import Faculty, Department, Lecturer, Group, \
                             Weekday, Week, SubgroupHelper, ItemNumberHelper
from timetable import db

import json, os
from collections import OrderedDict

CODES = [
    "OK",                                       # 0
    "Incorrect API Version",                    # 1
    "POST method not supported yet",            # 2
    "Unknown error",                            # 3
    "Reserve",                                  # 4
    "Reserve",                                  # 5
    "Unknown method",                           # 6
    "Method not support",                       # 7
    "Method not allowed",                       # 8
    "Method not found",                         # 9
    "Parameter \"query\" is empty",             # 10
    "Week is not correct",                      # 11
    "Weekday is not correct",                   # 12
    "Item number is not correct",               # 13
    "Parameter \"group_abbr\" is required",     # 14
    "Group not found",                          # 15
    "Parameter \"lecturer_id\" is required",    # 16
    "Lecturer not found",                       # 17
    
]

def error(code):
    if code > 0 and code < len(CODES):
        response = OrderedDict()
        
        response["response"] = None
        response["status"] = code
        response["message"] = CODES[code]
        
        return json.dumps(response, ensure_ascii=False, indent=4)
        
    resp_string = json.dumps(
                    OrderedDict([
                        ("response", None),
                        ("status", -1), 
                        ("message", "Internal Server Error")
                    ]), ensure_ascii=False, indent=4)
    return resp_string

def to_int(str, default=10):
    try:
        return int(str)
    except:
        pass
    return default
    
class v0_1(object):
    
    def __init__(self):
        self.METHODS = {
            "get": self._get,
            "search": self._search,
            "getLessons": self._get_lessons
        }
        
        self.ENTITYS_GET = {
            "faculties": self._get_faculties,
            "departments": self._get_departments,
            "lecturers": self._get_lecturers,
            "groups": self._get_groups
        }
        
        self.ENTITYS_SEARCH = {
            "faculties": self._search_faculties,
            "departments": self._search_departments,
            "lecturers": self._search_lecturers,
            "groups": self._search_groups
        }
        
        self.ENTITYS_GET_LESSONS = {
            "lecturer": self._get_lessons_lecturer,
            "group": self._get_lessons_group
        }
        
        self.ENTITYS = {
            "get": self.ENTITYS_GET,
            "search": self.ENTITYS_SEARCH,
            "getLessons": self.ENTITYS_GET_LESSONS
        }
    
        
        self.MAX_COUNT = 50
        
        self.ORDER = {
            "random": "random",
            "name": "name"
        }
        
        self.ROOT = os.environ["SERVER_NAME"]
        self.IMG_PATH = "/static/images/faculty_logo/"
    
    def execute(self, entity, method, args):
        # input method return json-string
                
        if not (method in self.METHODS):
            return error(6)
        if not (method in self.ENTITYS):
            return error(7)
        if not (entity in self.ENTITYS[method]):
            return error(8)
            
        return self.METHODS[method](entity, args)

    
    def _get(self, e, a):
        handle_func = self.ENTITYS_GET[e]
        offset = to_int(a.get("offset", 0))
        count = to_int(a.get("count", 10))
        order = a.get("order", self.ORDER["random"])

        if count > self.MAX_COUNT:
            count = self.MAX_COUNT
        
        if offset <= 0:
            offset = 0
                    
        if not (order in self.ORDER):
            order = self.ORDER["random"]
        
        return handle_func(offset, count, order, a)
        
    def _get_faculties(self, offset, count, order, a):
        try:
            faculties = Faculty.objects.skip(offset).limit(count)
            if len(faculties) == 0:
                r = self.get_excellent_dict()
                r["response"] = []
                return self.dump_dict(r)
            
            
            if order == self.ORDER["name"]:
                faculties = sorted(faculties, key=lambda i: i.title)
            
            r = self.get_excellent_dict()
            r["response"] = []
            for i in faculties:
                f = OrderedDict()
                f["abbr"] = i.abbr
                f["title"] = i.title
                f["description"] = i.description
                f["img"] = "http://{}{}{}.gif".format(self.ROOT, self.IMG_PATH, i.abbr)
                r["response"].append(f)
            
            return self.dump_dict(r)
        except Exception, e:
            #return str(e)
            return error(3)
            
    def _get_departments(self, offset, count, order, a):
        try:
            departments = Department.objects.skip(offset).limit(count)
            if len(departments) == 0:
                r = self.get_excellent_dict()
                r["response"] = []
                return self.dump_dict(r)
            
            
            if order == self.ORDER["name"]:
                departments = sorted(departments, key=lambda i: i.title)
            
            r = self.get_excellent_dict()
            r["response"] = []
            for i in departments:
                f = OrderedDict()
                f["abbr"] = i.abbr
                f["title"] = i.title
                f["description"] = i.description
                r["response"].append(f)
            
            return self.dump_dict(r)
        except Exception, e:
            #return str(e)
            return error(3)
            
            
    def _get_lecturers(self, offset, count, order, a):
        try:
            lecturers = Lecturer.objects.skip(offset).limit(count)
            if len(lecturers) == 0:
                r = self.get_excellent_dict()
                r["response"] = []
                return self.dump_dict(r)
            
            
            if order == self.ORDER["name"]:
                lecturers = sorted(lecturers, key=lambda i: i.name)
            
            r = self.get_excellent_dict()
            r["response"] = []
            for i in lecturers:
                f = OrderedDict()
                f["id"] = str(i.id)
                f["name"] = i.name
                f["degree"] = i.degree
                r["response"].append(f)
            
            return self.dump_dict(r)
        except Exception, e:
            #return str(e)
            return error(3)
        
        
        
    def _get_groups(self, offset, count, order, a):
        try:
            groups = Group.objects.skip(offset).limit(count)
            if len(groups) == 0:
                r = self.get_excellent_dict()
                r["response"] = []
                return self.dump_dict(r)
            
            
            if order == self.ORDER["name"]:
                groups = sorted(groups, key=lambda i: i.name)
            
            r = self.get_excellent_dict()
            r["response"] = []
            for i in groups:
                f = OrderedDict()
                f["abbr"] = i.abbr
                f["title"] = i.title
                f["description"] = i.description
                r["response"].append(f)
            
            return self.dump_dict(r)
        except Exception, e:
            #return str(e)
            return error(3)



    
    def _search(self, e, a):
        handle_func = self.ENTITYS_SEARCH[e]
        count = to_int(a.get("count", 10))
        query = a.get("query", "")
        
        if query == "":
            return error(10)
        
        if count > self.MAX_COUNT:
            count = self.MAX_COUNT
        
        
        return handle_func(query, count, a)
    
    
    def _search_faculties(self, query, count, a):
        try:
            faculties = Faculty.objects(db.Q(title__icontains=query) | 
                                        db.Q(description__icontains=query)).limit(count)
            if len(faculties) == 0:
                r = self.get_excellent_dict()
                r["response"] = []
                return self.dump_dict(r)
            
                        
            r = self.get_excellent_dict()
            r["response"] = []
            for i in faculties:
                f = OrderedDict()
                f["abbr"] = i.abbr
                f["title"] = i.title
                f["description"] = i.description
                f["img"] = "http://{}{}{}.gif".format(self.ROOT, self.IMG_PATH, i.abbr)
                r["response"].append(f)
            
            return self.dump_dict(r)
        except Exception, e:
            #return str(e)
            return error(3)
            
    def _search_departments(self, query, count, a):
        try:
            departments = Department.objects(db.Q(title__icontains=query) | 
                                             db.Q(description__icontains=query)).limit(count)
            if len(departments) == 0:
                r = self.get_excellent_dict()
                r["response"] = []
                return self.dump_dict(r)
            
                        
            r = self.get_excellent_dict()
            r["response"] = []
            for i in departments:
                f = OrderedDict()
                f["abbr"] = i.abbr
                f["title"] = i.title
                f["description"] = i.description
                r["response"].append(f)
            
            return self.dump_dict(r)
        except Exception, e:
            #return str(e)
            return error(3)
            
    def _search_lecturers(self, query, count, a):
        try:
            lecturers = Lecturer.objects(db.Q(name__icontains=query) | 
                                         db.Q(degree__icontains=query)).limit(count)
            if len(lecturers) == 0:
                r = self.get_excellent_dict()
                r["response"] = []
                return self.dump_dict(r)
            
                        
            r = self.get_excellent_dict()
            r["response"] = []
            for i in lecturers:
                f = OrderedDict()
                f["id"] = str(i.id)
                f["name"] = i.name
                f["degree"] = i.degree
                r["response"].append(f)
            
            return self.dump_dict(r)
        except Exception, e:
            return str(e)
            return error(3)
            
            
    def _search_groups(self, query, count, a):
        try:
            groups = Group.objects(db.Q(title__icontains=query) | 
                                   db.Q(description__icontains=query)).limit(count)
            if len(groups) == 0:
                r = self.get_excellent_dict()
                r["response"] = []
                return self.dump_dict(r)
            
                        
            r = self.get_excellent_dict()
            r["response"] = []
            for i in groups:
                f = OrderedDict()
                f["abbr"] = i.abbr
                f["title"] = i.title
                f["description"] = i.description
                r["response"].append(f)
            
            return self.dump_dict(r)
        except Exception, e:
            #return str(e)
            return error(3)
     
     
    def _get_lessons(self, e, a):
        handle_func = self.ENTITYS_GET_LESSONS[e]
        week = to_int(a.get("week", Week.ALL))
        weekday = to_int(a.get("weekday", Weekday.ALL))
        item_number = to_int(a.get("item_number", ItemNumberHelper.ALL))
        
        if not Week.is_correct(week):
            return error(11)
        
        if not Weekday.is_correct(weekday):
            return error(12)
        
        if not ItemNumberHelper.is_correct(item_number):
            return error(13)
        
        return handle_func(week, weekday, item_number, a)
    
    def _get_lessons_lecturer(self, week, weekday, item_number, a):
        try:
            
            lecturer_id = a.get("lecturer_id", "")
            if lecturer_id == "":
                return error(16)
            
            lecturer = None
            try:    
                lecturer = Lecturer.objects(id=lecturer_id).first()
            except Exception:
                pass
            if lecturer == None:
                return error(17)
            
            r = self.get_excellent_dict()
            r["response"] = OrderedDict()
            r["response"]["id"] = str(lecturer.id)
            r["response"]["name"] = lecturer.name
            
            r["response"]["lessons"] = []
            
            lessons = lecturer.lessons
            
            if week != Week.ALL:
                lessons = filter(lambda i: i.week == week, lessons)
                
            if weekday != Weekday.ALL:
                lessons = filter(lambda i: i.weekday == weekday, lessons)
                
            if item_number != ItemNumberHelper.ALL:
                lessons = filter(lambda i: i.item_number == item_number, lessons)
  
            for i in lessons:
                try:
                    l = OrderedDict()
                    l["title"] = i.title
                    l["room"] = i.room
                    l["item_number"] = i.item_number
                    l["weekday_number"] = i.weekday
                    l["weekday"] = Weekday.get_string(i.weekday)
                    l["week_number"] = i.week
                    l["week"] = Week.get_string(i.week)
                    l["description"] = i.description
                    
                    l["groups"] = []
                    
                    for j in i.subgroups:
                        try:
                            s = OrderedDict()
                            s["abbr"] = j.group.abbr
                            s["title"] = j.group.title
                            l["groups"].append(s)
                        except Exception:
                            pass
    
                    r["response"]["lessons"].append(l)
                except Exception:
                        pass
                    
            return self.dump_dict(r)
        except Exception, e:
            #return str(e)
            return error(3)
        
        
    def _get_lessons_group(self, week, weekday, item_number, a):
        try:
        
            group_abbr = a.get("group_abbr", "")
            
            if group_abbr == "":
                return error(14)
        
            group = Group.objects(abbr=group_abbr).first()
            if group == None:
                return error(15)
                
            r = self.get_excellent_dict()
            r["response"] = OrderedDict()
            r["response"]["abbr"] = group.abbr
            r["response"]["title"] = group.title
            
            r["response"]["lessons"] = []
            
            lessons = group.lessons
            
            if week != Week.ALL:
                lessons = filter(lambda i: i.week == week, lessons)
                
            if weekday != Weekday.ALL:
                lessons = filter(lambda i: i.weekday == weekday, lessons)
            
            if item_number != ItemNumberHelper.ALL:
                lessons = filter(lambda i: i.item_number == item_number, lessons)
            
            for i in lessons:           
                l = OrderedDict()
                l["title"] = i.title
                l["room"] = i.room
                l["lecturer"] = i.lecturer.name
                l["item_number"] = i.item_number
                l["weekday_number"] = i.weekday
                l["weekday"] = Weekday.get_string(i.weekday)
                l["week_number"] = i.week
                l["week"] = Week.get_string(i.week)
                l["description"] = i.description
                r["response"]["lessons"].append(l)
            
            return self.dump_dict(r)
        except Exception, e:
            #return str(e)
            return error(3)


    
    def get_excellent_dict(self):
        response = OrderedDict()
        
        response["response"] = None
        response["status"] = 0
        response["message"] = CODES[0]
        return response

    def dump_dict(self, r):
        return json.dumps(r, ensure_ascii=False, indent=4)
        
        
    def test_json(self):
        cs = {}
        knt = Faculty.objects(abbr="cs").first()
        cs["title"] = knt.title
        cs["abbr"] = knt.abbr
        cs["description"] = knt.description
        cs["ver"] = "0.1"
        cs["groups"] = []
        for g in knt.groups:
            cs["groups"].append({"title": g.title, "abbr": g.abbr, "description": g.description}) 
        return json.dumps(cs, ensure_ascii=False, indent=4)

class v0_2(object):

    def execute(self, entity, method, args):
        # input method return json-string
        pass
        
        
    def test_json(self):
        cs = {}
        knt = Faculty.objects(abbr="cs").first()
        cs["title"] = knt.title
        cs["abbr"] = knt.abbr
        cs["description"] = knt.description
        cs["ver"] = "0.2"
        cs["groups"] = []
        for g in knt.groups:
            cs["groups"].append({"title": g.title, "abbr": g.abbr, "description": g.description}) 
        return json.dumps(cs, ensure_ascii=False, indent=4)