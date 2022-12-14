from operator import indexOf
import string
import dotenv
import os
import canvasapi
import GMCommonFuncs as com
import pprint
import json
from flask import Flask, request, render_template

BASEURL = 'https://kent.instructure.com'
baseToken = "CANVAS_API_TOKEN_"

class User : 
  def __init__(self,name) : 
    name = name.replace(" ", '')
    name = name.upper()
    combineNameToken = baseToken + name
    TOKEN = os.environ.get(combineNameToken, 0)
    if (not TOKEN) :
      com.ERROR_HANDLER(1, name)
    canvas = canvasapi.Canvas(BASEURL, TOKEN)
    user = canvas.get_user('self')
    #Assign User attributes
    self.canvas = canvas
    self.user = user
    self.enrollments = self.user.get_enrollments(enrollment_state='active')
    self.courses = self.canvas.get_courses(enrollment_state='active')
  


def byName(user) : 

  enroll = user.enrollments

  courses = user.courses

  courses = com.sort(enroll, courses)

  courseList = [] 

  index = 1
  for i in courses :
    courseList.append(i.id)
    print(index, i, sep = ". ")
    index = index + 1

  index = index - 1
  id = int(input('Enter number course to view course specific options, or 0 to view all current grades: '))
  if (id > index or id < 0) : 
    print("Error: Invalid index")
    exit(-1)

  if (id <= index and id != 0) :
    id = courseList[id - 1]

  if (id == 0) : 
    for i,j in zip(courses, enroll) : 
      print(i.name, j.grades, end = "\n\n")

  if (id != 0) :
    options = ["Current Grade", "Current Points", "Current Score"]
    optionsAPI = ["current_grade", "current_points", "current_score"]
    print("Select from the following options: ")
    index = 1
    for i in options : 
      print(index, i, sep = ". ")
      index = index + 1

    optionsChoice = int(input("Input: "))
    optionsChoice = optionsChoice - 1

    for i in courses : 
      if (id == i.id) : 
        print(i.name)

    for i in enroll :
      if (id == i.course_id) :
        if (optionsAPI[optionsChoice] in i.grades) :
          print(i.grades[optionsAPI[optionsChoice]])
        else :
          print(i.grades)

def averageGrade() : 
  averages = []
  allNames = ["ASHTONCORSELLO", "GADIBANDLER"]
  for member in allNames : 
    getToken = baseToken + member
    TOKEN = os.environ.get(getToken, 0)
    canvas_api = canvasapi.Canvas(BASEURL, TOKEN)
    user = canvas_api.get_user('self')
    courses = user.get_enrollments(enrollment_state='active') 
    amt = 0
    average = 0
    for course in courses : 
      if ('current_grade' in course.grades and isinstance(course.grades['current_score'],float)) :
        average += course.grades["current_score"]
        amt = amt + 1
    average = average / amt
    averages.append(average)

  result = 0
  for i in averages : 
    result += i
  result /= len(averages)
  print("average = ", result)

def gradeBelow(minGrade, allNames) : 
  result = dict()
  for index, member in enumerate(allNames, start=1) : 
    com.LOADING(index, len(allNames))
    getToken = baseToken + member
    TOKEN = os.environ.get(getToken, 0)
    canvas_api = canvasapi.Canvas(BASEURL, TOKEN)
    user = canvas_api.get_user('self')
    courses = user.get_enrollments(enrollment_state='active') 
    classNames = user.get_courses(enrollment_state="active")
    classNames = com.sort(courses, classNames)
    for name, course in zip(classNames,courses) : 
      if ('current_score' in course.grades and isinstance(course.grades['current_score'],float)) :
        if (course.grades['current_score'] <= minGrade) :
          if (user not in result) : 
            result[user] = []
          strGrade = str(course.grades['current_score'])
          result[user].append(str(name.name + ' = ' + strGrade + '%'))
  
  for k, d in result.items() : 
    print(k)
    for i in d : 
      print('\t',i, end='\n')
  
  return json.dumps(result)
