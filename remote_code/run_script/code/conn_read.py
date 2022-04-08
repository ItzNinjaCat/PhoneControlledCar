import netifaces as ni
import os
file = open(os.path.dirname(os.getcwd())+ '/options/connections.txt', "r")
lines = file.readlines()
flask_port = lines.pop()
info_flag = lines.pop()
ctrl_socket_port = lines.pop()
security_flag = lines.pop()

ip =  ""
while True:
	try:
		ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
		break
	except:
		pass

security_flag = security_flag[security_flag.find("=") + 1:security_flag.find("#")].strip()
ctrl_socket_port = ctrl_socket_port[ctrl_socket_port.find("=") + 1:ctrl_socket_port.find("#")].strip()
info_flag = info_flag[info_flag.find("=") + 1:info_flag.find("#")].strip()
flask_port = flask_port[flask_port.find("=") + 1:flask_port.find("#")].strip()

def getSecurityFlag():
	if int(security_flag):
		return True
	else:
		return False

def getInfoFlag():
	if int(info_flag):
		return True
	else:
		return False
		
def getIp():
	return str(ip)

def getCtrlSocketPort():
	return int(ctrl_socket_port)

def getFlaskPort():
	return int(flask_port)
