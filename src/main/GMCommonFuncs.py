def LOADING(cur, total) : 
  print("Loading:", int(((cur/total)*100)), '%', end='\r')

def ERROR_HANDLER(code, info) :
  if (code == 1) :
    print("Fatal Error 1: Invalid Name [" + info +  "] Not Found. Terminating...")
    exit()

#Sorts courses in same order of enrollments to match up when showing all grades
#TODO: Optimize (cur: O(n^2))
def sort(enroll, courses) :
  result = []
  for i in enroll : 
    for j in courses : 
      if (i.course_id == j.id) :
        result.append(j)
      
  return result
