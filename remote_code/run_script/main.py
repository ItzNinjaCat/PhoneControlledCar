from flask import Flask, render_template, Response, request, jsonify
from gevent.pywsgi import WSGIServer
import time
import RPi.GPIO as GPIO
from camera import VideoCamera
from controls_server import destroy, setup, run_ctrl_server, distance
from conn_read import getIp, getCtrlSocketPort, getFlaskPort
from threading import Thread
from bs4 import BeautifulSoup

cam = Camera()

app = Flask(__name__)

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/dist', methods=['GET'])
def dist():
    return jsonify(distance())

@app.route('/')
def video_feed():
    return Response(gen(cam), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    setup()
    try:
        controls_socket_thread =  Thread(target=run_ctrl_server,args=(getIp(), getCtrlSocketPort()))
        controls_socket_thread.start()
        wsgi_server = WSGIServer((getIp(),getFlaskPort()), app)
        print(f"Flask server is running at http://{getIp()}:{getFlaskPort()}/")
        wsgi_server.serve_forever()
    except KeyboardInterrupt:
        try:
            destroy()
        except:
            pass
