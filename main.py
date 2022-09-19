from operator import indexOf
import string
import dotenv
import os
import canvasapi
import wx

dotenv.load_dotenv(dotenv.find_dotenv())
BASEURL = 'https://kent.instructure.com'
baseToken = "CANVAS_API_TOKEN_"
startOptions = ["Grades By Name", "Average Grade"]

#Sorts courses in same order of enrollments to match up when showing all grades
#TODO: Optimize (cur: O(n^2))
def sort(enroll, courses) :
  result = []
  for i in enroll : 
    for j in courses : 
      if (i.course_id == j.id) :
        result.append(j)
      
  return result


def byName() : 
  nameToken = input("Enter name: ")
  nameToken = nameToken.replace(" ", '')
  nameToken = nameToken.upper()
  getToken = baseToken + nameToken

  TOKEN = os.environ.get(getToken, 0)
  if not TOKEN : 
    print("Error: No user with name " + nameToken + " exists.")
    exit(-1)

  canvas_api = canvasapi.Canvas(BASEURL, TOKEN)

  result = canvas_api.get_user('self')
  print(result)

  enroll = result.get_enrollments(enrollment_state='active')

  courses = canvas_api.get_courses(enrollment_state='active')

  courses = sort(enroll, courses)

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
  allNames = ["enterName"]
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


index = 1
for i in startOptions : 
  print(index, i, sep = ". ")
  index = index + 1
start = int(input("Input: "))
if (start == 1) :
  byName()
if (start == 2) :
  averageGrade()



