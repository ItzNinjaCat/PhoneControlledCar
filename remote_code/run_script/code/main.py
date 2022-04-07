from flask import Flask, render_template, Response, request, jsonify, abort
from gevent.pywsgi import WSGIServer
import time
import RPi.GPIO as GPIO
from camera import Camera
from controls_server import destroy, setup, run_ctrl_server, distance
from conn_read import getIp, getCtrlSocketPort, getFlaskPort, getSecurityFlag
from threading import Thread
from bs4 import BeautifulSoup
import arpreq
import os
cam = Camera()

app = Flask(__name__)

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.before_request
def limit_remote_addr():
	if getSecurityFlag():
		mac = arpreq.arpreq(request.remote_addr)
		file = open(os.path.dirname(os.getcwd()) + '/options/trusted.txt')
		lines = file.readlines()
		string_list = ""
		for line in lines:
			string_list += line
		string_list.replace("\n", "")
		list = string_list.split(",")
		trusted = [s.strip() for s in list]
		if mac not in trusted:
			return abort(403)
		else:
			return


@app.route('/dist', methods=['GET'])
def dist():
    return jsonify(distance())

@app.route('/')
def video_feed():
    return Response(gen(cam), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    setup()
    try:
        controls_socket_thread =  Thread(target=run_ctrl_server,args=(getIp(), getCtrlSocketPort(), getSecurityFlag()))
        controls_socket_thread.start()
        wsgi_server = WSGIServer((getIp(),getFlaskPort()), app)
        print(f"Flask server is running at http://{getIp()}:{getFlaskPort()}/")
        wsgi_server.serve_forever()
    except KeyboardInterrupt:
        try:
            destroy()
        except:
            pass
