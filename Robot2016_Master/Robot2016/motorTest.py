#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import serial
import time
import atexit
#initialize i2c communication with motor shield
roboMotor = Adafruit_MotorHAT(addr=0x60)

#initialize serial communications with XBee RF reciever
xBee = serial.Serial('/dev/ttyACM1',57600)
compass = serial.Serial('/dev/ttyACM0', 9600)

def turnOffMotors():
	roboMotor.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	roboMotor.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

#create motor objects
leftFrontRear = roboMotor.getMotor(3)
rightFrontRear = roboMotor.getMotor(4)

#set speed to start ---- 0(off) - 255(Max)



#beacon navigation
def beaconNavigation():
	bHeadings = []
	botHeadings = []

	for x in range(0,2):
		botHeading = compass.readline()
		botHeading = float(botHeading)
		botHeadings.append(botHeading)
		print(botHeading)
		
	
		beaconHeading = xBee.readline()
		beaconHeading = float(beaconHeading)
		bHeadings.append(beaconHeading)
		print(beaconHeading)
		
	

	botTotal = sum(botHeadings)
	botLength = len(botHeadings)
	avgBotHeading = botTotal / botLength
	print "avg bot heading: ",  avgBotHeading

	total = sum(bHeadings)
	l = len(bHeadings)
	avgHeading = total / l
	print "avg b heading: ",  avgHeading

	#calculate opposite heading
	x = avgHeading + 180
	oppositeHeading = x % 360
	oppositeHeading = float(oppositeHeading)
	
	print "opposite beacon heading: ",  oppositeHeading



#	while(botHeading <= oppositeHeading or botHeading >= oppositeHeading):
	while(botHeading < oppositeHeading or botHeading > oppositeHeading + 1.0):
		botHeading = compass.readline()
		botHeading = float(botHeading)
		print botHeading
	#	rightRotate()


		forward()
#	toTheBeacon()
#for x in range(0,20):
#	heading = xBee.readline()
#	botBearing = compass.readline()
#	print(heading)
#	print(botBearing) 






#drive forwards
def forward():
#	beaconNavigation()

	while(True):
		leftFrontRear.setSpeed(80)
		rightFrontRear.setSpeed(80)
		leftFrontRear.run(Adafruit_MotorHAT.FORWARD)
		rightFrontRear.run(Adafruit_MotorHAT.FORWARD)

#drive backwards
def reverse():
	rightFrontRear.setSpeed(150)
	leftFrontRear.setSpeed(150)
	rightFrontRear.run(Adafruit_MotorHAT.BACKWARD)
	leftFrontRear.run(Adafruit_MotorHAT.BACKWARD)

#rotate left, rotate right
def leftRotate():
	rightFrontRear.setSpeed(70)
	rightFrontRear.run(Adafruit_MotorHAT.FORWARD)

def rightRotate():
	
	leftFrontRear.setSpeed(90)
	rightFrontRear.setSpeed(90)
	leftFrontRear.run(Adafruit_MotorHAT.FORWARD)
	rightFrontRear.run(Adafruit_MotorHAT.BACKWARD)
#turn left, turn right 
def leftTurn():
	rightFrontRear.setSpeed(200)
	leftFrontRear.setSpeed(125)
	rightFrontRear.run(Adafruit_MotorHAT.FORWARD)
	leftFrontRear.run(Adafruit_MotorHAT.FORWARD)

def rightTurn():
	rightFrontRear.setSpeed(150)
	leftFrontRear.setSpeed(200)
	leftFrontRear.run(Adafruit_MotorHAT.FORWARD)
	rightFrontRear.run(Adafruit_MotorHAT.FORWARD)


beaconNavigation()
forward()
