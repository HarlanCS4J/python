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
app.config["MONGO_URI"] = "mongodb://localhost:27017/shastaoutdoor"

affiliationDict={'student':StudentRoute,'teacher':TeacherRoute,'firstresponder':FirstResponderRoute,'military':MilitaryRoute}
templateIDs={"student":['5b4520d70455a91399295bec'],"military":['5b4503c8d3a2b414ca65bf9f'],"teacher":['5b44fc14d3a2b414ca65b18e'],"firstresponder":['5b450394d3a2b414ca65bef7']}
vargets={}
mongo = PyMongo(app)
dbase=mongo.db.transactions

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
	html=handleErrors(landingPage.getBody())
	return html

def get_var(self, *args):
	return vargets[arg[0]]

@app.route('/form_submit',methods=['POST'])
def form_submit():
	url="https://services-sandbox.sheerid.com/rest/0.5/verification"
	dataDict=dict(request.form.copy())
	headers={'Authorization':'Bearer '+os.getenv('SANDBOX_TOKEN')}
	source=request.form.get("source")
	dataDict['templateId']=templateIDs[source]
	print(headers)
	print(dataDict)
	
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
			output =  redirect('/'+source+'/success?couponCode='+couponCode+"&expiration="+exp.strftime('%b %d, %Y'))
			dataDict['couponCode']=couponCode
			dataDict['expiration']=exp.strftime('%b %d, %Y')
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
	headers={'Authorization':'Bearer '+os.getenv('SANDBOX_TOKEN')}
	source=request.form.get("source")
	dataDict['templateId']=templateIDs[source]
	
	req=requests.request('POST',url, headers=headers, data=dataDict)
	
	entry=dbase.find_one({'requestId':request.form.get('requestId')})
	entry['docReview']='submitted'
	dbase.replace_one({'requestId':request.form.get('requestId')},entry)

	return redirect('/'+source+'/uploadsuccess')

def get_var(self, *args):
	return vargets[arg[0]]

def handleErrors(html):
	if 'errorMessage' in request.args.keys():
		html = html.replace('<div class="error-container"> </div>','<div class="error-container"><p>Error: '+request.args.get('errorMessage')+'</p></div>')
	if 'couponCode' in request.args.keys():
		html = html.replace('##insert couponCode##',request.args.get('couponCode'))
		html = html.replace('##insert expiration##',request.args.get('expiration'))
	if 'requestId' in request.args.keys():
		requestId=request.args.get('requestId')
		reqLookUp = dbase.find_one({"requestId":requestId})
		html = html.replace('##insert username##',reqLookUp.get('FIRST_NAME')[0]+" "+reqLookUp.get('LAST_NAME')[0])
		html = html.replace('##insert school##',reqLookUp.get('organizationName')[0])
		html = html.replace('##insert requestId##',requestId)
		enlistment = reqLookUp.get('AFFILIATION')[0].replace("_"," ").title()
		html = html.replace('##insert status##',enlistment)
		
		url="https://services-sandbox.sheerid.com/rest/0.5/asset/token"
		req=requests.request('POST',url, headers={'Authorization':'Bearer '+os.getenv('SANDBOX_TOKEN')}, data={'requestId':requestId})
		req=req.json()
		print (req)
		assetToken = req.get('token')

		html = html.replace('##insert assetToken##',assetToken)
	return html
