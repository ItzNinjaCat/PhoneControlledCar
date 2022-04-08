import RPi.GPIO as GPIO
import time

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

def forwardON():
	GPIO.output(MotorForward,GPIO.HIGH)
def forwardOFF():
	GPIO.output(MotorForward,GPIO.LOW)

def backwardON():
	GPIO.output(MotorBackward,GPIO.HIGH)
def backwardOFF():
	GPIO.output(MotorBackward,GPIO.LOW)
	
def rightON():
	GPIO.output(MotorRigth,GPIO.HIGH)
def rightOFF():
	GPIO.output(MotorRigth,GPIO.LOW)
	
def leftON():
	GPIO.output(MotorLeft,GPIO.HIGH)
def leftOFF():
	GPIO.output(MotorLeft,GPIO.LOW)
	