from gevent.pywsgi import WSGIServer
from threading import Thread

from controls_server import run_ctrl_server
from conn_read import getIp, getCtrlSocketPort, getFlaskPort, getSecurityFlag, getInfoFlag
from GPIO_handling import setup, destroy, forwardOFF, backwardOFF, rightOFF, leftOFF
from video_dist_server import app

if __name__ == '__main__':
	setup()
	try:
		if getInfoFlag():
			controls_socket_thread =  Thread(target=run_ctrl_server,args=(getIp(), getCtrlSocketPort(), getSecurityFlag()))
			controls_socket_thread.start()
			wsgi_server = WSGIServer((getIp(),getFlaskPort()), app)
			print(f"Flask server is running at http://{getIp()}:{getFlaskPort()}/")
			wsgi_server.serve_forever()
		else:
			run_ctrl_server(getIp(), getCtrlSocketPort(), getSecurityFlag())
	except:
		try:
			forwardOFF()
			backwardOFF()
			rightOFF()
			leftOFF()
			control_socket_thread._stop()
			destroy()
		except:
			pass
