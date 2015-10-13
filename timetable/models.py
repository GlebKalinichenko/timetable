# -*- coding: utf-8 -*-
from timetable import db

class Lecturer(db.Document):
    name = db.StringField(max_length=100, required=True)                    # ФИО
    degree = db.StringField(max_length=50, default="Старший преподаватель") # Должность
    department = db.ReferenceField('Department', required=True)             # Кафедра
    lessons = db.ListField(db.ReferenceField('Lesson'))                     # Пары
    
class Faculty(db.Document):
    title = db.StringField(max_length=10, required=True)              # КНТ (название на русском)
    abbr = db.StringField(max_length=5, required=True, unique=True)   # cs (аббривиатура с англ. Computer science)
    description = db.StringField(max_length=500)                      # Описание факультета (полное название)
    departments = db.ListField(db.ReferenceField('Department'))       # Кафедры
    groups = db.ListField(db.ReferenceField('Group'))                 # Группы
    
class Department(db.Document):
    title = db.StringField(max_length=100, required=True)           # Название на русском
    abbr = db.StringField(max_length=5, required=True, unique=True) # pmi (аббривиатура с англ)
    description = db.StringField(max_length=500)                    # Описание кафедры
    lecturers = db.ListField(db.ReferenceField('Lecturer'))         # Преподаватели на кафедре

class Group(db.Document):
    title = db.StringField(max_length=10, required=True)              # ПИ-12а (название на русском)
    abbr = db.StringField(max_length=5, required=True, unique=True)   # pi (аббривиатура с англ)
    description = db.StringField(max_length=500)                      # Описание группы
    faculty = db.ReferenceField('Faculty', required=True)             # Факультет
    lessons = db.ListField(db.ReferenceField('Lesson'))               # Пары
    
class Lesson(db.Document):
    title = db.StringField(max_length=100, required=True)                   # Название предмета на русском
    room = db.StringField(max_length=10, required=True)                     # 8.705 (Номер аудитории)
    item_number = db.IntField(min_value=1, max_value=7, required=True)      # Номер пары (1, 2, 3, 4, 5)
    weekday = db.IntField(min_value=1, max_value=7, required=True)          # День недели (пн=1, вт=2, ср=3, ...)
    week = db.IntField(min_value=0, max_value=2, required=True, default=0)  # Неделя(верхняя=1, нижняя=2, любая=0)
    subgroup = db.IntField(min_value=0, max_value=4, required=True, default=0) # Подгруппа 0 - вся группа (0, 1, 2, 3, 4 ...)
    group = db.ReferenceField('Group', required=True)
    lecturer = db.ReferenceField('Lecturer', required=True)
   