from flask import Flask, redirect, url_for, render_template, session
import os.path
import sys

#viewSwitch = {"about"}
#sys.path.insert(0,'./routes/')


class StudentRoute:
	html=""
	output=""
	affiliation="student"
	
	def __init__(self, *args):
		if len(args)==0:
			self.html='something.html'
		elif len(args)==1:
			if args[0]=='verify':
				self.html=render_template(self.affiliation+'Verify.html')
			elif args[0]=='uploadsuccess':
				self.html=render_template(self.affiliation+'UploadSuccess.html')
			elif args[0]=='success':
				self.html=render_template(self.affiliation+'Success.html')
		elif len(args)==2:
			if args[0]=='upload':
				session = args[1]
				username = session['FIRST_NAME'][0]+" "+session["LAST_NAME"][0]
				school = session['organizationName'][0]
				submitToken = session['submitToken']
				requestId = session['requestId']
				self.html=render_template(self.affiliation+'Upload.html', username=username, school=school, submitToken=submitToken, requestId=requestId)
			else:
				self.html=render_template(self.affiliation+'Verify.html')
				html=html.replace("<!--Errors go here-->","<B>Error: </B>"+args[0]+"<BR><B>Message: </B>"+args[1])
		else:
			self.html=render_template(self.affiliation+'Verify.html')
			html=html.replace("<!--Errors go here-->","<B>Error: </B>Invalid arguments"+"<BR><B>Message: </B>"+[msg+", " for msg in args])

	app = Flask(__name__, template_folder='../views/partials')

	def getBody(self):
		return self.html
