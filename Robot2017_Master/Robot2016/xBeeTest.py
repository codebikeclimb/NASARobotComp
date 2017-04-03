#!/usr/bin/python
import serial
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
 
import time
import atexit

mh = Adafruit_MotorHAT(addr=0x60)

def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
 
atexit.register(turnOffMotors)

rightFrontRear = mh.getMotor(3)
leftFrontRear = mh.getMotor(1)
rightFrontRear.setSpeed(1)
leftFrontRear.setSpeed(1)

#initialize serial communications with XBee RF reciever
xBee = serial.Serial('/dev/ttyACM0',57600)
#initialize serial communications with onboard compass
compass = serial.Serial('/dev/ttyACM1', 9600)
#compass = serial.Serial('/dev/ttyACM1', 9600)
done = False
beaconHeadings = []
signalList = []
botHeadings = []

def getSignals():
    for i in range (0,9):
        xBee_serial = xBee.readline().strip() # read serial input from arduino and remove trailing \n character
        h, s = xBee_serial.split(",")        #split serial input into two lists
        #beaconHeadings.append(h)
        signalList.append(s)
    return signalList

#get beacon headings from the xbee
def getHeadings():
    for i in range (0,9):
        xBee_serial = xBee.readline()
        h, s = xBee_serial.split(",")
        beaconHeadings.append(h)
    #signalList.append(s)
    return beaconHeadings

def leftRotate():
    rightFrontRear.setSpeed(70)
    rightFrontRear.run(Adafruit_MotorHAT.FORWARD)


def rightRotate():
    leftFrontRear.setSpeed(90)
    rightFrontRear.setSpeed(90)
    leftFrontRear.run(Adafruit_MotorHAT.FORWARD)
    rightFrontRear.run(Adafruit_MotorHAT.BACKWARD)

def forward():
    print "forward!"
    leftFrontRear.setSpeed(80)
    rightFrontRear.setSpeed(80)
    leftFrontRear.run(Adafruit_MotorHAT.FORWARD)
    rightFrontRear.run(Adafruit_MotorHAT.FORWARD)


def getBotHeading():
	botHeadings = []
	#for i in range (0,9):
    	botHeading = compass.readline()
    	botHeading = int(botHeading)
    	#	botHeadings.append(botHeading)
    		# print(botHeading)
	return botHeading

        #find the avg bot compass reading
       # botTotal = sum(botHeadings)
        #botLength = len(botHeadings)
        #avgBotHeading = botTotal / botLength
        #return avgBotHeading

def findHeading():
    getBotHeading()	
    getSignals()
    getHeadings()
    
    #calculate the correct beacon heading using the max Signal Strength index
    maxSignalIndex = signalList.index(max(signalList))
    correctHeadingIndex = maxSignalIndex
    correctHeading = beaconHeadings[correctHeadingIndex]

    # calculate opposite heading
    x = int(correctHeading) + 180
    oppositeHeading = x % 360

    findBeacon(oppositeHeading)

def findBeacon(cHeading):
	success = False
	bHeading = getBotHeading()

	print "cHeading: " + str(cHeading)
	       # print botHeading
        while (bHeading >= cHeading + 5 or bHeading <= cHeading - 5):
		#print getBotHeading()
                bHeading = getBotHeading()
		print bHeading	
		rightRotate()
	success = True   
        forward()

while not done:
#   bHeading = getBotHeading()     
   findHeading()
