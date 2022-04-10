from flask import Flask, render_template, Response, request, jsonify, abort
from gevent.pywsgi import WSGIServer
from camera import Camera
import arpreq
import os

from conn_read import getSecurityFlag

from GPIO_handling import distance

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
			abort(403)


@app.route('/dist', methods=['GET'])
def dist():
    return jsonify(distance())

@app.route('/')
def video_feed():
    return Response(gen(cam), mimetype='multipart/x-mixed-replace; boundary=frame')
