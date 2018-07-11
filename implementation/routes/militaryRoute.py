from flask import Flask, redirect, url_for, render_template 
import os.path
import sys

#viewSwitch = {"about"}
#sys.path.insert(0,'./routes/')

class MilitaryRoute:
	html=""
	output=""
	affiliation="military"
	
	def __init__(self, *args):
		if len(args)==0:
			self.html='something.html'
		elif len(args)==1:
			if args[0]=='verify':
				self.html=render_template(self.affiliation+'Verify.html')
			elif args[0]=='upload':
				self.html=render_template(self.affiliation+'Upload.html')
			elif args[0]=='uploadsuccess':
				self.html=render_template(self.affiliation+'UploadSuccess.html')
			elif args[0]=='success':
				self.html=render_template(self.affiliation+'Success.html')
		elif len(args)==2:
			self.body=self.loadBody("<B>Error: </B>"+args[0], "<B>Message: </B>"+args[1])
		else:
			self.body=self.loadBody("<B>Error: </B>Invalid arguments", "<B>Message: </B>"+[msg for msg in args])

	app = Flask(__name__, template_folder='../views/partials')

	def getBody(self):
		return self.html