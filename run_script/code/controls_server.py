import socket
from threading import Thread
import time
import arpreq
import os

from GPIO_handling import forwardON, forwardOFF, backwardON, backwardOFF, rightON, rightOFF, leftON, leftOFF

def recv_messages(conn, address):
    try:
        while True:
            message = conn.recv(1024).decode()
            print(message)
            if message == "q":
		print(f"Connection from {address} has been lost")
                conn.close()
                forwardOFF()
                backwardOFF()
                rightOFF()
                leftOFF()		
                return
            elif message == "forwardON":
                forwardON()
            elif message == "forwardOFF":
                forwardOFF()
            elif message == "backwardON":
               backwardON()
            elif message == "backwardOFF":
                backwardOFF()
            elif message == "rightON":
                rightON()
            elif message == "rightOFF":
                rightOFF()
            elif message == "leftON":
                leftON()
            elif message == "leftOFF":
                leftOFF()
    except:
        conn.close()
        forwardOFF()
        backwardOFF()
        rightOFF()
        leftOFF()
        print(f"Connection from {address} has been lost")
        return

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
	print(f"Controls server is running at {ip}:{port}")
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

