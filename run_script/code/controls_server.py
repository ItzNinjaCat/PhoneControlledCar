import socket
from threading import Thread
import RPi.GPIO as GPIO
import time
import arpreq
import os
MotorForward = 25
MotorBackward = 24

MotorRigth = 12
MotorLeft = 6


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
	mac = arpreq.arpreq(conn[0])
	file = open(os.path.dirname(os.getcwd()) + '/options/trusted.txt', "r")
	lines = file.readlines()
	string_list = ""
	for line in lines:
		string_list += line
	string_list = string_list.replace("\n", "")
	list = string_list.split(",")
	trusted_addresses = [s.strip() for s in list]
	if mac in trusted_addresses:
		return True
	else:
		return False



def run_ctrl_server(ip, port, security_flag):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((ip, port))
	sock.listen(5)
	print(f" Controls server is running at {ip}:{port}")
	#setup()
	try:
		while True:
			clientsocket, address = sock.accept()
			if security_flag:
				if not security_check(address):
					print(f"Connection from {address} has been refused because it is not whitelisted")
					clientsocket.close()
					continue
				else:
					print(f"Connection from {address} has been established")
					client_control_thread = Thread(target=recv_messages,args=(clientsocket,address))
					client_control_thread.start()
			else:
				print(f"Connection from {address} has been established")
				client_control_thread = Thread(target=recv_messages,args=(clientsocket,address))
				client_control_thread.start()
	except KeyboardInterrupt:
		try:
			destroy()
		except:
			pass
