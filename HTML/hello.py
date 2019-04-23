#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 18:44:13 2019

@author: Lucifer
"""

from flask import Flask ,render_template
import sqlite3


app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World ! this is flask!"

@app.route('/Goodbye')
def zaijian():
    return "See you next time!"
    
@app.route('/sample')
def template_demo():
    return render_template('test.html', 
                           title = 'Stevens',
                           my_header = 'Stevens Repository',
                           my_param = "Yo,what's up!")

@app.route('/result')
def number_of_students():

    DB_file = '/Users/apple/Desktop/Code/810/810_star_up.db'

    db = sqlite3.connect(DB_file)

    query = """select HW11_instructors.CWID,HW11_instructors.Name,HW11_instructors.Dept,HW11_grades.Course,count(HW11_grades.Student_CWID) as students
            from HW11_instructors left join HW11_grades on HW11_instructors.CWID = HW11_grades.Instructor_CWID
            group by HW11_instructors.CWID,HW11_instructors.Name,HW11_instructors.Dept,HW11_grades.Course
            order by students DESC """
    result = db.execute(query)

    data = [{'cwid': CWID, 'name': Name, 'depart': Dept, 'course': Course, 'students':Students}
            for CWID, Name, Dept, Course, Students in result]

    db.close()

    return render_template('students.html',
                            title = 'Stevens Institute of Technology',
                            header = 'Stevens Repository',
                            table_title = 'Number of students by course and instructor',
                            instructors = data)

app.run(debug=True)