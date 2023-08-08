from operator import indexOf
import sys
import dotenv
import os
import canvasapi
import GradeManager as GM
import json
from flask import Flask, request, render_template, url_for, redirect, session, Markup
from dataclasses import replace
import sqlite3
import string
import random
import hashlib

from flaskwebgui import FlaskUI

#import psycopg2
#connect to database
#conn = psycopg2.connect(
#    database="sqlite3",
#    user="acorsell",
#    password="secret",p
#    host="localhost",
#    port='5432'
#)
#cur = conn.cursor()

appdir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

conn = sqlite3.connect(os.path.join(appdir, 'FATS.sqlite'), check_same_thread=False)
cur = conn.cursor()



#create flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index() :
    #if user is not logged in, redirect to login page
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template("index.html", session=session)


@app.route("/login/", methods=['GET','POST'])
def login():
    if request.method == 'POST' :
        email = request.form.get('email')
        password = request.form.get('password')
        #hash password
        passwordHash = hashlib.sha256(password.encode()).hexdigest()
        cur.execute("SELECT * FROM fats WHERE email = ?", (email,))
        data = cur.fetchall()
        #if email is not registered, return error
        if (len(data) == 0) :
            error = Markup('<div class="alert alert-danger" role="alert"> Invalid Email or Password </div>')
            return render_template("login.html", error=error)
        #if email is registered, check if user is an admin
        #elif (data[0][6] != True) :
          #  return render_template("login.html", error="Not an Admin")
        #if email is registered, check if password is correct
        elif (data[0][7] != passwordHash) :
            #error is markdown red box with text "Invalid Password"
            error = Markup('<div class="alert alert-danger" role="alert"> Invalid Email or Password </div>')
            return render_template("login.html", error=error)
        else :
            #if email is registered, password is correct, and user is an admin, create session
            session['logged_in'] = True
            session['first_name'] = data[0][1]
            session['last_name'] = data[0][2]
            session['email'] = email
            #session['password'] = password
            session['databaseid'] = data[0][8]
            #login successful, redirect to index (home page)
            return redirect(url_for('index'))
    return render_template("login.html")


@app.route("/register/", methods=['GET','POST'])
def register():
    if request.method == 'POST' :
        email = request.form.get('email')
        #check if email is already registered
        cur.execute("SELECT * FROM fats WHERE email = ?", (email,))
        data = cur.fetchall()
        #if email is already registered, return error
        if (len(data) != 0) :
            return render_template("register.html", error="Email Already Registered")
        password = request.form.get('password')
        passwordCheck = request.form.get('passwordCheck')
        #check if passwords match
        if (password != passwordCheck) :
            return render_template("register.html", error="Passwords Do Not Match")
        passwordHash = hashlib.sha256(password.encode()).hexdigest()
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        #generate random databse token with 8 numbers followed by 15 letters
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
        token = str(random.randint(10000000, 99999999)) + token
        #check if token is already in use
        cur.execute("SELECT * FROM fats WHERE databaseid = ?", (token,))
        data = cur.fetchall()
        #if token is in use, generate a new one
        while (len(data) != 0) :
            token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
            token = str(random.randint(10000000, 99999999)) + token
            cur.execute("SELECT * FROM fats WHERE databaseid = ?", (token,))
            data = cur.fetchall()
        #insert new user into database
        cur.execute("INSERT INTO fats (first_name, last_name, email, canvas_token, pledge, admin, password, databaseid) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (firstName, lastName, email, 0, 0, 1, passwordHash, token,))
        conn.commit()
        return render_template("register.html", error="Registration Successful")
    return render_template("register.html", error = "test")

#@app.route("/gradeBelow/", methods=['GET','POST'])
#def gradeBelow():
#    if request.method == 'POST' :
#        grade = request.form.get('grade')
#       brothersBox = request.form.get('brothers')
#        pledgesBox = request.form.get('pledges')
#   if (brothersBox != None and pledgesBox == None) :
#      # group = brothers
#    elif (brothersBox == None and pledgesBox != None) :
#       # group = pledges
#    else :
#       # group = allNames
#    #ata = GM.gradeBelow(int(grade),group)
#    #sonTree = json.loads(data)
#   # return render_template('./index.html', data=jsonTree)


@app.route("/byName/", methods=['GET','POST'])
def byName():
    if request.method == 'POST' :
        name = request.form.get('name')
    result = GM.byName(GM.User(name))
    result = json.loads(result)
    return render_template('/index.html', nameData=result)


@app.route("/allNames/", methods=['GET','POST'])
def allNames():
    #if user is not logged in, redirect to login page
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    #show all names in database that have the same databaseid as the user
    cur.execute("SELECT first_name, last_name, email, pledge, id FROM fats WHERE databaseid = ? AND admin = false", (session['databaseid'],))
    data = cur.fetchall()
    return render_template('/tables.html', allNames=data)


@app.route('/addUser/', methods=['GET','POST'])
def addUser():
    #if user is not logged in, redirect to login page
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST' :
        #get form data
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        token = request.form.get('canvasToken')
        pledge = request.form.get('pledge')
        if (pledge == None) :
            pledge = 0
        else :
            pledge = 1
        pledge = bool(pledge)
        password = "NULL" #default password
        #insert new user into database
        try:
            cur.execute("INSERT INTO FATS (first_name, last_name, email, canvas_token, pledge, admin, password, databaseid) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (firstName, lastName, email, token, pledge, bool(0), password,session['databaseid'])); 
            conn.commit()
            success = Markup('<div class="alert alert-success" role="alert">User Added Successfully</div>')
            return render_template('/addUser.html', error=success)
        except Exception as e:
            error = Markup('<div class="alert alert-danger" role="alert">Error Adding User</div>')
            return render_template('/addUser.html', error=error)
    return render_template('/addUser.html')


@app.route('/viewUser/', methods=['GET','POST'])
def viewUser():
    session['editID'] = request.form.get('user')
    return redirect(url_for('editUser'))


@app.route('/editUser/', methods=['GET','POST'])
def editUser():
    #if user is not logged in, redirect to login page
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    #get user data from database
    cur.execute("SELECT first_name, last_name, email, canvas_token, pledge, id FROM fats WHERE id = ?", (session['editID'],))
    data = cur.fetchall()
    return render_template('/editUser.html', userData=data)


@app.route('/updateUser/', methods=['GET','POST'])
def updateUser():
    if request.method == 'POST' : 
        #get form data
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        token = request.form.get('canvasToken')
        #update database
        if (firstName != None) :
            #check if field is empty
            if (firstName == "") :
                return redirect(url_for('editUser'))
            cur.execute("UPDATE fats SET first_name = ? WHERE id = ?", (firstName, session['editID'],))
            conn.commit()
            return redirect(url_for('editUser'))
        if (lastName != None) :
            #check if field is empty
            if (lastName == "") :
                return redirect(url_for('editUser'))
            cur.execute("UPDATE fats SET last_name = ? WHERE id = ?", (lastName, session['editID'],))
            conn.commit()
            return redirect(url_for('editUser'))
        if (email != None) :
            #check if field is empty
            if (email == "") :
                return redirect(url_for('editUser'))
            cur.execute("UPDATE fats SET email = ? WHERE id = ?", (email, session['editID'],))
            conn.commit()
            return redirect(url_for('editUser'))
        if (token != None) :
            #check if field is empty
            if (token == "") :
                return redirect(url_for('editUser'))
            cur.execute("UPDATE fats SET canvas_token = ? WHERE id = ?", (token, session['editID'],))
            conn.commit()
            return redirect(url_for('editUser'))
        #update pledge status if other fields are empty
        pledge = request.form.get('pledge')
        if (pledge != None) :
            pledge = 1
        else :
            pledge = 0
        pledge = bool(pledge)
        cur.execute("UPDATE fats SET pledge = ? WHERE id = ?", (pledge, session['editID'],))
        conn.commit()
        return redirect(url_for('editUser'))
        
        
@app.route('/removeUser/', methods=['GET','POST'])
def removeUser():
    if request.method == 'POST' :
        ID = request.form.get('user')
        cur.execute("DELETE FROM FATS WHERE id = ?", (ID,)); 
        conn.commit()
    return redirect(url_for('allNames'))

@app.route('/viewIndGrades/', methods=['GET','POST'])
def viewIndGrades():
    #if user is not logged in, redirect to login page
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    #set session viewID to user id
    session['viewID'] = request.form.get('user')
    #get canvas token from user id
    cur.execute("SELECT canvas_token FROM fats WHERE id = ?", (session['viewID'],))
    token = cur.fetchall()
    data = GM.byName(GM.User(token[0][0]))
    return render_template('/viewIndGrades.html', userData=data)

if __name__ == "__main__":
  #app.run(debug=True)
  FlaskUI(app=app, server="flask").run()


#dotenv.load_dotenv(dotenv.find_dotenv())
#BASEURL = 'https://kent.instructure.com'
#baseToken = "CANVAS_API_TOKEN_"
#startOptions = ["Grades By Name", "Average Grade", "Low Grades"]

#brothers = ["ASHTONCORSELLO", "GADIBANDLER", "CALEBPETTI", "COOPERERNST", "JACOBFAIRBEND",
#             "DEVINCORRAO", "VINCEPATRONE", "JACKNOVOTNY", "MAXKOLUDER", "NATEKOOISTRA",
#              "JOELCASEY", "JOEYWEBER", "BRANDONFISHER", "LUCASDEWIT", "ANDREWMONTAMBO", "BRYSONANDERSON",
#               "CONNORBROWN", "MASONEVANS", "AIDANZAK", "ZACHFLIGNER", "ROBERTDEFAZIO", 
#               "LUKESMITH"]
#pledges = ["DOMINICPALMA", "DENNYDIXON", "SPENCERLEHRIAN", "MATTHART",
#               "JACOBPROUT", "CHRISTIANHOCH", "DRAYDENWINNING", "ZACHSIMMONS", 
#               "ALEXKOLUDER", "NICKSNIDER"]
#allNames = brothers + pledges

#FUNCTIONCALLED = sys.argv[1]

#if (FUNCTIONCALLED == '1') : 
#    GM.byName(GM.User(sys.argv[2]))
#elif (FUNCTIONCALLED == '2' ) :  #Prints a list of people and their corresponding classes with grade =< gradeMin
#    gradeMin = int(sys.argv[2])
#    if(sys.argv[3] == '-a') :
#        db = allNames
#    if(sys.argv[3] == '-b') :
#        db = brothers
#    if(sys.argv[3] == '-p') :
#        db = pledges
#    GM.gradeBelow(gradeMin, db)
