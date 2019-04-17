'''
Created: 2019-04-01 16:42:54
Author : Jia Wen
Email : jwen6@stevens.edu
Description: Repository
'''
from HW08JiaWen import file_reader
from prettytable import PrettyTable
from collections import defaultdict
import sqlite3
import unittest
import os

class Majors:
    
    pt_hdr = ['Dept','Required','Electives']

    def __init__(self,major):
        self._major = major
        self._update_type = defaultdict(list)

    def update_major(self, type, course):
        self._updete_type[type].append(course)

    def required_course(self):
        return self._update_type['R']

    def elective_course(self):
        return self._update_type['E']

    def prettytable(self):
        yield self._major, self.required_course(), self.elective_course()

class Students:

    pt_hdr = ['CWID','Name','Major','Completed Course','Remaining Required','Remaining Electives']
    
    def __init__(self,CWID,name,major):
        """class Students contains student ID, name and major"""

        self._CWID = CWID
        self._name = name
        self._major = major
        self._grade = dict()
        self._remain_re_list = []
        self._remain_el_list = []

    def add_grade(self,course,grade):
        if grade in ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', '']:
            self._grade[course] = grade

    def check_completed(self, course):
        if course not in self._grade:
            return True
        else:
            if self._grade[course] not in ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', '']:
                return True
        
    def prettytable(self):
        if len(self._remain_el_list) == 0:
            yield self._CWID, self._name, self._major,sorted(list(self._grade)), self._remain_re_list, 'None'
        else:
            yield self._CWID, self._name, self._major,sorted(list(self._grade)), self._remain_re_list, self._remain_el_list

class Instructors:
    
    pt_hdr = ['CWID','Name','Dept','Course','Students']

    def __init__(self,CWID,name,department):
        """class Instructors contains instructor ID, name and department"""
        
        self._CWID = CWID 
        self._name = name
        self._department = department
        self._num = defaultdict(int)

    def add_student(self,course):
        self._num[course] += 1
    
    def prettytable(self):
        for course,students in self._num.items():
            yield self._CWID,self._name,self._department,course,students


class University:
    
    def __init__(self,path):
        """define three pathes to get the file of students , instructors and grades"""
        
        self._students_file= os.path.join(path,'students.txt')
        self._instructors_file = os.path.join(path,'instructors.txt')
        self._grades_file = os.path.join(path,'grades.txt')
        self._majors_file = os.path.join(path, 'majors.txt')
        self._students = {}
        self._instructors = {}
        self._majors= {}
    
    def read_majors(self):
        for major, type, course in file_reader(self._majors_file, 3, '\t', False):
            self._majors[major] = Majors(major)
        """
        try:
            fp = open(self._majors_file,'r')
        except:
            raise FileNotFoundError(f"FileNotFoundError: can not open {self._majors_file}")
        else:
            with fp:
                sf_re = set()
                sf_el = set()
                sy_re = set()
                sy_el = set()
                for line in fp:
                    newline = line.rstrip('\n').strip('\t').split('\t')
                    if newline[0] == 'SFEN' and newline[1] =='R':
                        sf_re.add(newline[2])
                    elif newline[0] == 'SFEN' and newline[1] == 'E':
                        sf_el.add(newline[2])
                    elif newline[0] == 'SYEN' and newline[1] == 'R':
                        sy_re.add(newline[2])
                    elif newline[0] == 'SYEN' and newline[1] == 'E':
                        sy_el.add(newline[2])
        for major in self._majors.keys():
            if major == 'SFEN':
                Majors[major].append(sf_re)
            if major == 'SYEN':
                Majors[major].add_required_course(sy_re).add_elective_course(sy_el)
        """
        for major, type, course in file_reader(self._majors_file, 3, '\t', False):
            self._majors[major]._update_type[type].append(course)

    def add_remain(self):
        for temp_student in self._students.values():
            try:
                for course in self._majors[temp_student._major].required_course():
                    if temp_student.check_completed(course):
                        temp_student._remain_re_list.append(course)
            
                for course in self._majors[temp_student._major].elective_course():
                    if not temp_student.check_completed(course):
                        break
                else:
                    temp_student._remain_el_list.extend(self._majors[temp_student._major].elective_course())
                    
            except KeyError as e:
                raise KeyError(f"there is no {e} dept")

    def read_students(self):
        """read students.txt and get all the information about single student
           and store all the elements in students dict"""
        for CWID,name,major in file_reader(self._students_file, 3, '\t', False):
            self._students[CWID] = Students(CWID,name,major)

    def read_instructors(self):
        """read instructors.txt and get all the information about single instructor
           and store all the elements in instructors dict"""

        for CWID,name,department in file_reader(self._instructors_file, 3, '\t',False):
            self._instructors[CWID] = Instructors(CWID,name,department)

    def read_grades(self):
        """read grades.txt and get all the information about single student's all releated grades
           and store all the elements in grades dict"""

        for CWID,course,grade,instructor in file_reader(self._grades_file, 4, '\t', False):
            if CWID in self._students.keys():
                self._students[CWID].add_grade(course,grade)

            if instructor in self._instructors.keys():
                self._instructors[instructor].add_student(course)

    def majors_summary(self):
        table = PrettyTable(Majors.pt_hdr)
        for dept in self._majors.values():
            for major, re, el in dept.prettytable():
                table.add_row([major, re, el])
        print("Majors Summary:")
        print(table)
        return table
    
    def students_summary(self):
        table = PrettyTable(Students.pt_hdr)
        for temp_students in self._students.values():
            for cwid,name,major,com_course,re,el in temp_students.prettytable():
                table.add_row([cwid,name,major,com_course,re,el])
        print("Students Summary:")
        print(table)
        return table

    def instructors_summary(self):
        table = PrettyTable(Instructors.pt_hdr)
        for tran_instructors in self._instructors.values():
            for cwid, name, department, course, students in tran_instructors.prettytable():
                table.add_row([cwid,name,department,course,students])
        print("Instructors Summary:")
        print(table)
        return table

def main():
    path = '/Users/apple/Desktop/Source code/810'
    result = University(path)
    result.read_majors()
    result.read_students()
    result.read_instructors()
    result.read_grades()
    result.add_remain()
    result.majors_summary()
    result.students_summary()
    result.instructors_summary()
    DB_file = '/Users/apple/Desktop/Code/810/810_star_up.db'
    db = sqlite3.connect(DB_file)
    table = PrettyTable(['CWID','Name','Dept','Teaching Course','Number of Students'])
    query = """select HW11_instructors.CWID,HW11_instructors.Name,HW11_instructors.Dept,HW11_grades.Course,count(HW11_grades.Student_CWID) as students
            from HW11_instructors left join HW11_grades on HW11_instructors.CWID = HW11_grades.Instructor_CWID
            group by HW11_instructors.CWID,HW11_instructors.Name,HW11_instructors.Dept,HW11_grades.Course
            order by students DESC """
    for file in db.execute(query):
        table.add_row(file)
    print(table)

    db.close()

class AssignmentTest(unittest.TestCase):
    def test_student_summary(self):
        path = '/Users/apple/Desktop/Source code/810'   
        result = University(path)
        result.read_majors()
        result.read_students()
        result.read_instructors()
        result.read_grades()
        result.add_remain()
        pt = PrettyTable(field_names=['CWID', 'Name', 'Major','Completed Courses', 'Remaining Required', 'Remaining Elective'])
        test_student_summary = []
        test_student_summary.append(
            ('10103', 'Baldwin, C', 'SFEN', "['CS 501', 'SSW 564', 'SSW 567', 'SSW 687']", "['SSW 540', 'SSW 555']","None"))
        test_student_summary.append(
            ('10115', 'Wyatt, X', 'SFEN', "['CS 545', 'SSW 564', 'SSW 567', 'SSW 687']", "['SSW 540', 'SSW 555']", "None"))
        test_student_summary.append(
            ('10172', 'Forbes, I', 'SFEN', "['SSW 555', 'SSW 567']", "['SSW 540', 'SSW 564']", "['CS 501', 'CS 513', 'CS 545']"))
        test_student_summary.append(
            ("10175", 'Erickson, D', 'SFEN', "['SSW 564', 'SSW 567', 'SSW 687']", "['SSW 540', 'SSW 555']", "['CS 501', 'CS 513', 'CS 545']"))
        test_student_summary.append(
            ("10183", "Chapman, O", 'SFEN', "['SSW 689']", "['SSW 540', 'SSW 564', 'SSW 555', 'SSW 567']", "['CS 501', 'CS 513', 'CS 545']"))
        test_student_summary.append(
            ("11399", "Cordova, I", 'SYEN', "['SSW 540']", "['SYS 671', 'SYS 612', 'SYS 800']","None"))
        test_student_summary.append(
            ("11461", "Wright, U", 'SYEN', "['SYS 611', 'SYS 750', 'SYS 800']", "['SYS 671', 'SYS 612']", "['SSW 810', 'SSW 540', 'SSW 565']"))
        test_student_summary.append(
            ("11658", "Kelly, P", 'SYEN', "[]", "['SYS 671', 'SYS 612', 'SYS 800']", "['SSW 810', 'SSW 540', 'SSW 565']"))
        test_student_summary.append(
            ("11714", "Morton, A", 'SYEN', "['SYS 611', 'SYS 645']", "['SYS 671', 'SYS 612', 'SYS 800']", "['SSW 810', 'SSW 540', 'SSW 565']"))
        test_student_summary.append(
            ("11788", "Fuller, E", 'SYEN', "['SSW 540']", "['SYS 671', 'SYS 612', 'SYS 800']", "None"))
        for CWID, name, major, com_course ,re, el in test_student_summary:
            pt.add_row([CWID, name, major, com_course, re, el])
        self.assertEqual(str(result.students_summary()), str(pt))

    def test_major_summary(self):
        path = '/Users/apple/Desktop/Source code/810'   
        result = University(path)
        result.read_majors()
        result.read_students()
        result.read_instructors()
        result.read_grades()
        result.add_remain()
        pt = PrettyTable(field_names=['Dept', 'Required', 'Electives'])
        test_major_summary = []
        test_major_summary.append(
            ("SFEN", "['SSW 540', 'SSW 564', 'SSW 555', 'SSW 567']", "['CS 501', 'CS 513', 'CS 545']"))
        test_major_summary.append(
            ("SYEN", "['SYS 671', 'SYS 612', 'SYS 800']", "['SSW 810', 'SSW 540', 'SSW 565']"))

        for dept, required_course, elective_course in test_major_summary:
            pt.add_row([dept, required_course, elective_course])
        
        self.assertEqual(str(result.major_summary()), str(pt))

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
    main()