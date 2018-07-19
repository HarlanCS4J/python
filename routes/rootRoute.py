from flask import Flask, redirect, url_for, request, render_template
import sys

#viewSwitch = {"about"}
#sys.path.insert(0,'./routes/')
rootViews = {'index.html':'root.html','verify':'verify.html'}
class RootRoute:
	affiliation = "{none}"

	def __init__(self, *args):
		if len(args)==0:
			self.html=render_template('root.html')
		elif len(args)==1:
			self.html=render_template(rootViews[args[0]])
		elif len(args)==2:
			self.html=render_template('root.html').replace('<!--Errors go here-->',"<B>Error: </B>"+args[0]+"<br><B>Message: </B>"+args[1])
		else:
			self.html=render_template('root.html').replace('<!--Errors go here-->',"<B>Error: </B>Invalid arguments<br><B>Message: </B>"+[msg for msg in args])

	app = Flask(__name__, template_folder='../views')

	def getBody(self):
		return self.html

	def loadBody(self,*args):
		self.output="<body background='../static/star-wars-wallpaper-hd.jpg'>"\
			"<TABLE>"\
			"<TR><TH colspan=5>PATHS</TH>"\
			"<TR><TD>"\
			"<a href='/'>Root Path</A></TD>"\
			"<TD>"\
			"<a href='/student/'>Student Path</A></TD>"\
			"<TD>"\
			"<a href='/military/'>Military Path</A></TD>"\
			"<TD>"\
			"<a href='/firstresponder/'>1st Responder Path</A></TD>"\
			"<TD>"\
			"<a href='/teacher/'>Teacher Path</A></TD>"\
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

