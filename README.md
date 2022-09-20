# GradeManager

#### Utilizing the Canvas API [https://canvas.instructure.com/doc/api/], Grade Manager makes it easy to view, maintain, and analyze students grades. Currently, this program can show individual grades via search by name, and also find the average grade of all current participants. The possibilites are endless for what analysis you can do with this easily retrievable data.

## Setup
#### Setting up this program to use with your organisation is quick and easy. 
### Steps
##### 1. In main.py, change the BASEURL to your Universities Canvas URL.
##### 2. In .env, change 'TOKEN' to the users Canvas Token, and 'NAME' in the key to the users name. 
###### Note: In order to use Average Grade, you must add all user names into the 'allnames' array in the averageGrade function. This will be changed soon, so check back shortly for an easier method. 
