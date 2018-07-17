from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
import sys, datetime, requests, os, json


sys.path.insert(0,'./routes/')
from studentRoute import StudentRoute
from rootRoute import RootRoute
from militaryRoute import MilitaryRoute
from teacherRoute import TeacherRoute
from firstResponderRoute import FirstResponderRoute

#variables
app = Flask(__name__, template_folder='templates')
app.config["MONGO_URI"] = os.environ['MONGODB_URI']

affiliationDict={'student':StudentRoute,'teacher':TeacherRoute,'firstresponder':FirstResponderRoute,'military':MilitaryRoute}
templateIDs={"student":['5b4520d70455a91399295bec'],"military":['5b4503c8d3a2b414ca65bf9f'],"teacher":['5b44fc14d3a2b414ca65b18e'],"firstresponder":['5b450394d3a2b414ca65bef7']}
vargets={}
mongo = PyMongo(app)
dbase=mongo.db.transactions
bearerToken=os.environ['SANDBOX_TOKEN']

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
	return redirect('/'+affiliation+'/verify')

@app.route("/<affiliation>/<view>")
def routeTraffic(affiliation, view):
	vargets['goat']="cow"
	if affiliation in affiliationDict.keys():
		landingPage=affiliationDict[affiliation](view)
	else:
		landingPage=RootRoute("URL-Error", request.url)
	return landingPage.getBody()

def get_var(self, *args):
	return vargets[arg[0]]

@app.route('/form_submit',methods=['POST'])
def form_submit():
	url="https://services-sandbox.sheerid.com/rest/0.5/verification"
	dataDict=dict(request.form.copy())
	headers={'Authorization':'Bearer '+bearerToken}
	source=request.form.get("source")
	dataDict['templateId']=templateIDs[source]
	
	req=requests.request('POST',url, headers=headers, data=dataDict)
	jsonDict=req.json()
	status=jsonDict.get('status')
	if status=="COMPLETE":
		reqId=jsonDict.get("requestId")
		result=jsonDict.get("result")
		dataDict['requestId']=reqId
		dataDict['_id']=reqId
		dataDict['result']=result

		if result==True:
			print ('---------------------------------------------OUTPUT----------------------------------------------')
			coupon=jsonDict.get('metadata')
			if 'couponCode' in coupon.keys():
				print(coupon)
				couponCode=coupon.get('couponCode')
				expiration=coupon.get('expiration')
			else:
				couponCode='COUPON_ERROR'
				expiration = -1
			exp=datetime.date.today()+datetime.timedelta(days=int(expiration))
			expString = exp.strftime('%b %d, %Y')
			output =  redirect('/'+source+'/success?couponCode='+couponCode+"&expiration="+expString)
			dataDict['couponCode']=couponCode
			dataDict['expiration']=expString
		else:
			output = redirect('/'+source+'/upload?requestId='+reqId)
			dataDict['docReview']='unsubmitted'
	elif status=="400":
		output = redirect('/'+source+'/verify?errorMessage='+jsonDict.get("message"))
		dataDict['result']=''
	dbase.insert(dataDict)
	return output

@app.route('/doc_review',methods=['POST'])
def doc_review():
	url="https://services-sandbox.sheerid.com/rest/0.5/asset/token"
	dataDict=dict(request.form.copy())
	headers={'Authorization':'Bearer '+bearerToken}
	source=request.form.get("source")
	dataDict['templateId']=templateIDs[source]
	
	req=requests.request('POST',url, headers=headers, data=dataDict)
	
	entry=dbase.find_one({'requestId':request.form.get('requestId')})
	entry['docReview']='submitted'
	dbase.replace_one({'requestId':request.form.get('requestId')},entry)

	return redirect('/'+source+'/uploadsuccess')

def get_var(self, *args):
	return vargets[arg[0]]

def pullKey(dictIn,keyIn):
	if keyIn in dictIn.keys():
		return dictIn.get(keyIn)
	else:
		return ""

def stringReplace(stringIn, oldSub, newSub):
	if oldSub in stringIn:
		return stringIn.replace(oldSub, newSub)
	else:
		return stringIn