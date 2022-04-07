import socket
#import ssl
from threading import Thread
import RPi.GPIO as GPIO
import time
from subprocess import Popen, PIPE
import re
MotorForward = 25
MotorBackward = 24

MotorRigth = 6
MotorLeft = 12


Trigger= 4
Echo = 21


motor_arr = [MotorForward, MotorBackward, MotorRigth, MotorLeft, Trigger]

def setup():
    GPIO.setmode(GPIO.BCM)
    for motor in motor_arr:
        try:
            GPIO.setup(motor, GPIO.OUT)
        except:
            pass
    try:
        GPIO.setup(Echo, GPIO.IN)
    except:
        pass

def destroy():	
	GPIO.cleanup()

def distance():
	GPIO.output(Trigger, True)

	time.sleep(0.00001)
	GPIO.output(Trigger, False)

	start_time = time.time()
	stop_time = time.time()

	while GPIO.input(Echo) == 0:
		start_time = time.time()

	while GPIO.input(Echo) == 1:
		stop_time = time.time()

	time_passed = stop_time - start_time
	distance = (time_passed * 34300) / 2

	return distance

def recv_messages(conn, address):
    try:
        while True:
            message = conn.recv(1024).decode()
            print(message)
            if message == "q":
                break
            elif message == "forwardON":
                GPIO.output(MotorForward,GPIO.HIGH)
            elif message == "forwardOFF":
                GPIO.output(MotorForward,GPIO.LOW)
            elif message == "backwardON":
                GPIO.output(MotorBackward,GPIO.HIGH)
            elif message == "backwardOFF":
                GPIO.output(MotorBackward,GPIO.LOW)
            elif message == "rightON":
                GPIO.output(MotorRigth,GPIO.HIGH)
            elif message == "rightOFF":
                GPIO.output(MotorRigth,GPIO.LOW)
            elif message == "leftON":
                GPIO.output(MotorLeft,GPIO.HIGH)
            elif message == "leftOFF":
                GPIO.output(MotorLeft,GPIO.LOW)
    except KeyboardInterrupt:
        conn.close()
        GPIO.output(MotorForward,GPIO.LOW)
        GPIO.output(MotorBackward,GPIO.LOW)
        GPIO.output(MotorRigth,GPIO.LOW)
        GPIO.output(MotorLeft,GPIO.LOW)
        print(f"Connection from {address} has been lost")

def security_check(conn):
	pid = Popen(["arp", "-n", conn[0]], stdout=PIPE)
	s = pid.communicate()[0]
	mac = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", s).groups()[0]
	file = open(os.path.dirname(os.getcwd()) + '/options/trusted.txt', "r")
	string_list = file.split()
	trusted_adresses = [s.strip() for s in string_list]
	for addr in truste_addresses:
		if addr == mac:
			return True
	return False



def run_ctrl_server(ip, port, security_flag):
	wrapped_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#	wrapped_sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLS, ciphers="ADH-AES256-SHA")
	wrapped_sock.bind((ip, port))
	wrapped_sock.listen(5)
	print(f" Controls server is running at {ip}:{port}")
	#setup()
	try:
		while True:
			clientsocket, address = wrapped_sock.accept()
			if security_flag:
				if not security_check(address):
					connclientsocket.close()
					continue
#			client_distance_thread = Thread(target=send_distance,args=(clientsocket,))
#			client_distance_thread.start()
			print(f"Connection from {address} has been established")
			client_control_thread = Thread(target=recv_messages,args=(clientsocket,address))
			client_control_thread.start()
	except KeyboardInterrupt:
		try:
			destroy()
		except:
			pass
