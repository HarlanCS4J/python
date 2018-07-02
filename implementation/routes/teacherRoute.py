from flask import Flask, redirect, url_for, request
import sys

#viewSwitch = {"about"}
#sys.path.insert(0,'./routes/')

class TeacherRoute:
	output=""
	affiliation = "Teacher"

	def __init__(self, *args):
		if len(args)==0:
			self.body=self.loadBody("<B>Affiliation: </B>"+self.affiliation,"<B>View: </B>{none}")
		elif len(args)==1:
			self.body=self.loadBody("<B>Affiliation: </B>"+self.affiliation,"<B>View: </B>"+args[0])
		elif len(args)==2:
			self.body=self.loadBody("<B>Error: </B>"+args[0], "<B>Message: </B>"+args[1])
		else:
			self.body=self.loadBody("<B>Error: </B>Invalid arguments", "<B>Message: </B>"+[msg for msg in args])

	app = Flask(__name__, template_folder='../views')

	def getBody(self):
		return self.output

	def loadBody(self,*args):
		self.output="<body background='../static/star-wars-wallpaper-hd.jpg'>"\
			"<TABLE>"\
			"<TR><TH colspan=5>PATHS</TH>"\
			"<TR><TD>"\
			"<a href='http://127.0.0.1:5000/'>Root Path</A></TD>"\
			"<TD>"\
			"<a href='http://127.0.0.1:5000/student/'>Student Path</A></TD>"\
			"<TD>"\
			"<a href='http://127.0.0.1:5000/military/'>Military Path</A></TD>"\
			"<TD>"\
			"<a href='http://127.0.0.1:5000/firstresponder/'>1st Responder Path</A></TD>"\
			"<TD>"\
			"<a href='http://127.0.0.1:5000/teacher/'>Teacher Path</A></TD>"\
			"</TR>"\
			"<TR><TH colspan=5>FILES</TH>"\
			"<TR><TD>"\
			"<a href='about'>About Path</A></TD>"\
			"<TD>"\
			"<a href='offers'>Offers Path</A></TD>"\
			"<TD>"\
			"<a href='verify-landing'>Verify Path</A></TD>"\
			"<TD>"\
			"</TR>"\
			"<TR><TD>"\
			"<a href='redeem'>Redeem Path</A></TD>"\
			"<TD>"\
			"<a href='pending'>Pending Path</A></TD>"\
			"<TD>"\
			"<a href='notify'>Notify Path</A></TD>"\
			"</TR>"\
			"</TABLE><P><P>"+ "<p><p>" + args[0] + "<p>"+args[1]

