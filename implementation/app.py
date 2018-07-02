from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import sys

sys.path.insert(0,'./routes/')
from studentRoute import StudentRoute
from rootRoute import RootRoute
from militaryRoute import MilitaryRoute
from teacherRoute import TeacherRoute
from firstResponderRoute import FirstResponderRoute

# constants
#affiliationSwitch = {
	# 1:studentRoute(), 
	# 2:militaryRoute(),
	# 3:firstResponderRoute(),
	# 4:teacherRoute()}

#variables
app = Flask(__name__, template_folder='templates')
mongo = PyMongo(app)


@app.route("/")
def routeRoot():
	landingPage=RootRoute()
	return landingPage.getBody()

@app.route("/<view>")
def routeView(view):
	landingPage=RootRoute(view)
	return landingPage.getBody()

@app.route("/<affiliation>/")
def routeAffiliation(affiliation):
#	landingPage=affiliationSwitch.get(affiliation,rootRoute("URL-Error", request.url))
	if affiliation == "student":
		landingPage=StudentRoute()
	elif affiliation == "teacher":
		landingPage=TeacherRoute()
	elif affiliation == "firstresponder":
		landingPage=FirstResponderRoute()
	elif affiliation == "military":
		landingPage=MilitaryRoute()
	else:
		landingPage=RootRoute("URL-Error", request.url)
	return landingPage.getBody()

@app.route("/<affiliation>/<view>")
def routeTraffic(affiliation, view):
	if affiliation == "student":
		landingPage=StudentRoute(view)
	elif affiliation == "teacher":
		landingPage=TeacherRoute(view)
	elif affiliation == "firstresponder":
		landingPage=FirstResponderRoute(view)
	elif affiliation == "military":
		landingPage=MilitaryRoute(view)
	else:
		landingPage=RootRoute("URL-Error", request.url)
	return landingPage.getBody()
