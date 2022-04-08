import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

MotorForward = 25
MotorBackward = 24

MotorRight = 12
MotorLeft = 6


Trigger= 4
Echo = 21

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MotorForward, GPIO.OUT)
    GPIO.setup(MotorBackward, GPIO.OUT)
    GPIO.setup(MotorRight, GPIO.OUT)
    GPIO.setup(MotorLeft, GPIO.OUT)

    GPIO.setup(Trigger, GPIO.OUT)
    GPIO.setup(Echo, GPIO.IN)

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

def forwardON():
	GPIO.output(MotorForward,GPIO.HIGH)
def forwardOFF():
	GPIO.output(MotorForward,GPIO.LOW)

def backwardON():
	GPIO.output(MotorBackward,GPIO.HIGH)
def backwardOFF():
	GPIO.output(MotorBackward,GPIO.LOW)
	
def rightON():
	GPIO.output(MotorRight,GPIO.HIGH)
def rightOFF():
	GPIO.output(MotorRight,GPIO.LOW)
	
def leftON():
	GPIO.output(MotorLeft,GPIO.HIGH)
def leftOFF():
	GPIO.output(MotorLeft,GPIO.LOW)
	
