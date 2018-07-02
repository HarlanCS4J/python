# language conversion of verificationRequest.js
# URL: https://github.com/sheerid/getting-started/blob/master/implementation/models/verificationRequest.js
import logging

def getip():
	return '256.256.256.256'

logging.basicConfig(
	filename='./record.log',
	level=logging.INFO,
	format='%(asctime)s  %(clientip)s %(levelname)s: %(message)s') 
ip = { 'clientip' : getip()}
#logger = logging.getLogger("tcpserver")
logging.info("New Connection", extra=ip)
# logging.{level}('message') {level}=[critical, error, warning, info]


