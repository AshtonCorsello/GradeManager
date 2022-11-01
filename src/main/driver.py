from lib2to3.pgen2 import token
from operator import indexOf
import sys
import dotenv
import os
import canvasapi
import GradeManager as GM
import json
from flask import Flask, request, render_template

app = Flask(__name__)

dotenv.load_dotenv(dotenv.find_dotenv())
BASEURL = 'https://kent.instructure.com'
baseToken = "CANVAS_API_TOKEN_"
startOptions = ["Grades By Name", "Average Grade", "Low Grades"]

allNames = ["ASHTONCORSELLO", "GADIBANDLER", "CALEBPETTI", "COOPERERNST", "JACOBFAIRBEND",
              "DEVINCORRAO", "VINCEPATRONE", "JACKNOVOTNY", "MAXKOLUDER", "NATEKOOISTRA",
              "JOELCASEY", "JOEYWEBER", "BRANDONFISHER", "LUCASDEWIT", "ANDREWMONTAMBO", "BRYSONANDERSON",
               "CONNORBROWN", "MASONEVANS", "AIDANZAK", "ZACHFLIGNER", "ROBERTDEFAZIO", 
               "LUKESMITH", "DOMINICPALMA", "DENNYDIXON", "SPENCERLEHRIAN", "TREVONNEGILLISON", "MATTHART",
               "JACOBPROUT", "CHRISTIANHOCH", "LIAMSTEG", "DRAYDENWINNING", "ZACHSIMMONS", 
               "ALEXKOLUDER", "BRADLEYNORRIS", "NICKSNIDER", "RYANCHRISTIAN"]
brothers = ["ASHTONCORSELLO", "GADIBANDLER", "CALEBPETTI", "COOPERERNST", "JACOBFAIRBEND",
              "DEVINCORRAO", "VINCEPATRONE", "JACKNOVOTNY", "MAXKOLUDER", "NATEKOOISTRA",
              "JOELCASEY", "JOEYWEBER", "BRANDONFISHER", "LUCASDEWIT", "ANDREWMONTAMBO", "BRYSONANDERSON",
               "CONNORBROWN", "MASONEVANS", "AIDANZAK", "ZACHFLIGNER", "ROBERTDEFAZIO", 
               "LUKESMITH"]
pledges = ["DOMINICPALMA", "DENNYDIXON", "SPENCERLEHRIAN", "TREVONNEGILLISON", "MATTHART",
               "JACOBPROUT", "CHRISTIANHOCH", "LIAMSTEG", "DRAYDENWINNING", "ZACHSIMMONS", 
               "ALEXKOLUDER", "BRADLEYNORRIS", "NICKSNIDER", "RYANCHRISTIAN"]

FUNCTIONCALLED = sys.argv[1]

if (FUNCTIONCALLED == '1') : 
    GM.byName(GM.User(sys.argv[2]))
elif (FUNCTIONCALLED == '2' ) :  #Prints a list of people and their corresponding classes with grade =< gradeMin
    gradeMin = int(sys.argv[2])
    if(sys.argv[3] == '-a') :
        db = allNames
    if(sys.argv[3] == '-b') :
        db = brothers
    if(sys.argv[3] == '-p') :
        db = pledges
    GM.gradeBelow(gradeMin, db)
