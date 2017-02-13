#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import serial
import time
import atexit

#serial commands to arduino
COMMANDS = {
    "STOP_SERVO": 0x00,     #turn off servos on arduino
    "PAN_LEFT": 0x01,       #pan lidar to the leftmost position
    "PAN_RIGHT": 0x02,      #pan lidar to the rightmost position
    "PAN_CENTER": 0x03,     #pan lidar back to the center postion
    "SERVO_POS": 0x04,      #get servo position
    "READ_LIDAR": 0x05,     #get distance readings from the lidar
    "READ_COMPASS": 0X06,   #unused for now
}

done = False

signalList = []
botHeadings = []
beaconHeadings = []

#initialize i2c communication with motor shield
roboMotor = Adafruit_MotorHAT(addr=0x60)

#create motor objects
leftFrontRear = roboMotor.getMotor(3)
rightFrontRear = roboMotor.getMotor(4)

#initialize serial communications with XBee RF reciever
xBee_compass = serial.Serial('/dev/ttyACM1',57600)
lidar = serial.Serial('/dev/ttyACM0', 115200)

#robot control functions and AI code
########################################################################################################################

#send arduino lidar instructions
def sendCommandToLidar(x):
    lidar.write(x)

#send Fio xbee & compass instructions
def sendCommandToBeaconNavigation(x):
    xBee_compass.write(x)

#get signal strengths from the xbee
def getSignals():
    for i in range (0,9):
        xBee_serial = xBee_compass.readline().strip() # read serial input from arduino and remove trailing \n character
        h, s = xBee_serial.split(",")        #split serial input into two lists
        #beaconHeadings.append(h)
        signalList.append(s)
    return signalList

#get beacon headings from the xbee
def getHeadings():
    for i in range (0,9):
        xBee_serial = xBee_compass.readline()
        h, s = xBee_serial.split(",")
        beaconHeadings.append(h)
    #signalList.append(s)
    return beaconHeadings

#find the strongest signal from the beacon and get the heading, then calculate the opposite heading and pass that and bot heading to findBeacon()
def findHeading():
    #read bot compass
    botHeading = xBee_compass.readline()
    botHeading = int(botHeadings)
    botHeadings.append(botHeading)
    # print(botHeading)

    #find the avg bot compass reading
    botTotal = sum(botHeadings)
    botLength = len(botHeadings)
    avgBotHeading = botTotal / botLength
    #print "avg bot heading: ", avgBotHeading

    #get the beacon headings and signal strengths in 2 different lists
    getSignals()
    getHeadings()

    #calculate the correct beacon heading using the max Signal Strength index
    maxSignalIndex = max(signalList)
    correctHeadingIndex = maxSignalIndex
    correctHeading = beaconHeadings.index(correctHeadingIndex)

    # calculate opposite heading
    x = correctHeading + 180
    oppositeHeading = x % 360

    findBeacon(oppositeHeading, avgBotHeading)

#turn the bot towards the beacon and call obstacle avoidance
def findBeacon(cHeading, bHeading):

    #	while(botHeading <= oppositeHeading or botHeading >= oppositeHeading):
    while (bHeading > cHeading + 4 and bHeading < cHeading - 4):
        botHeading = xBee_compass.readline()
        botHeading = int(botHeading)
        print botHeading
        rightRotate()

    findWay();


#lidar obstacle avoidance
def findWay(self):
    distanceArray = []

    # pan left
    sendCommandToLidar(COMMANDS["PAN_LEFT"])
    time.sleep(1)
    distanceArray.append(sendCommandToLidar(COMMANDS["READ_LIDAR"]))
    #aux.writetofile('Pan Left Distace', distanceArray[0])

    # pan center
    sendCommandToLidar(COMMANDS["PAN_CENTER"])
    time.sleep(1)
    distanceArray.append(sendCommandToLidar(COMMANDS["READ_LIDAR"]))
    #aux.writetofile('Pan Center Distace', distanceArray[1])

    # pan right
    sendCommandToLidar(COMMANDS["PAN_RIGHT"])
    time.sleep(1)
    distanceArray.append(sendCommandToLidar(COMMANDS["READ_LIDAR"]))
    #aux.writetofile('Pan Right Distace', distanceArray[2])


    maxdistance = max(distanceArray)
    maxindex = distanceArray.index(maxdistance)

    if maxindex == 0:
        leftRotate()
        #aux.writetofile('Turning Left', distanceArray[maxindex])
    elif maxindex == 2:
        rightRotate()
        #aux.writetofile('Turning Right', distanceArray[maxindex])
    else:

        aux.writetofile('Not Turning', distanceArray[maxindex])

    del distanceArray[:]

#motor functions
########################################################################################################################
# drive forwards
def forward():
    print "forward!"
    leftFrontRear.setSpeed(80)
    rightFrontRear.setSpeed(80)
    leftFrontRear.run(Adafruit_MotorHAT.FORWARD)
    rightFrontRear.run(Adafruit_MotorHAT.FORWARD)


# drive backwards
def reverse():
    print "reverse!"
    rightFrontRear.setSpeed(150)
    leftFrontRear.setSpeed(150)
    rightFrontRear.run(Adafruit_MotorHAT.BACKWARD)
    leftFrontRear.run(Adafruit_MotorHAT.BACKWARD)


# rotate left, rotate right
def leftRotate():
    rightFrontRear.setSpeed(70)
    rightFrontRear.run(Adafruit_MotorHAT.FORWARD)


def rightRotate():
    leftFrontRear.setSpeed(90)
    rightFrontRear.setSpeed(90)
    leftFrontRear.run(Adafruit_MotorHAT.FORWARD)
    rightFrontRear.run(Adafruit_MotorHAT.BACKWARD)


# turn left, turn right
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

def turnOffMotors():
	roboMotor.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	roboMotor.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

#main control loop for beacon navigation, obstacle avoidance, and robot locomotion
########################################################################################################################

while not done:
    print "heyoo"