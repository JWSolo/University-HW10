'''
Created: 2019-04-01 16:42:54
Author : Jia Wen
Email : jwen6@stevens.edu
Description: Repository
'''
from HW08JiaWen import file_reader
from prettytable import PrettyTable
from collections import defaultdict
import unittest
import os


class Students:

    pt_hdr = ['CWID','Name','Completed Course']

    def __init__(self,CWID,name,major):
        """class Students contains student ID, name and major"""

        self._CWID = CWID
        self._name = name
        self._major = major
        self._grade = defaultdict(str)

    def add_grade(self,course,grade):
        self._grade[course] = grade
        
    def prettytable(self):
        yield self._CWID,self._name,sorted(list(self._grade))

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
        self._students = {}
        self._instructors = {}

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
    
    def students_summary(self):
        table = PrettyTable(Students.pt_hdr)
        for tran_students in self._students.values():
            for cwid,name,com_course in tran_students.prettytable():
                table.add_row([cwid,name,com_course])
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

class Test(unittest.TestCase):
    
    def test_students_summary(self):
        expected = {'10103': ['10103', 'Baldwin, C', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687']],
                    '10115': ['10115', 'Wyatt, X', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687']],
                    '10172': ['10172', 'Forbes, I', ['SSW 555', 'SSW 567']],
                    '10175': ['10175', 'Erickson, D', ['SSW 564', 'SSW 567', 'SSW 687']],
                    '10183': ['10183', 'Chapman, O', ['SSW 689']],                 
                    '11399': ['11399', 'Cordova, I', ['SSW 540']],                
                    '11461': ['11461', 'Wright, U', ['SYS 611', 'SYS 750', 'SYS 800']],    
                    '11658': ['11658', 'Kelly, P', ['SSW 540']],              
                    '11714': ['11714', 'Morton, A', ['SYS 611', 'SYS 645']],       
                    '11788': ['11788', 'Fuller, E', ['SSW 540']]} 
        
        result = {CWID: Students.prettytable.row() for CWID, Students in self.University._students.items()}
        self.assertEqual(expected,result)

def main():
    path = '/Users/apple/Desktop/Source code/810'
    result = University(path)
    result.read_students()
    result.read_instructors()
    result.read_grades()
    result.students_summary()
    result.instructors_summary()

if __name__ == "__main__":
    unittest.main(exit=False,verbosity=2)
    main()