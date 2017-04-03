#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import serial
import time
import atexit
import math

#serial commands to arduino
COMMANDS = {
    "STOP_SERVO": 0x00,
    "PAN_LEFT": 0x01,
    "PAN_RIGHT": 0x02,
    "PAN_CENTER": 0x03,
    "SERVO_POS": 0x04,
    "READ_BEACON": 0x05,
    "READ_COMPASS": 0X06,
}

done = False

signalList = []
botHeadings = []
beaconHeadings = []

#initialize i2c communication with motor shield
roboMotor = Adafruit_MotorHAT(addr=0x60)

#initialize i2c communication with robot compass
roboCompass = serial.Serial('/dev/ttyACM3', 9600)

#create motor objects
leftFrontRear = roboMotor.getMotor(1)
rightFrontRear = roboMotor.getMotor(3)

#initialize serial communications with XBee RF reciever
xBee_compass = serial.Serial('/dev/ttyACM1',57600)
lidar = serial.Serial('/dev/ttyACM0', 115200)

#robot control functions and AI code
########################################################################################################################

#send arduino lidar instructions
def sendCommandToLidar():
    lidar.write()

#send Fio xbee & compass instructions
def sendCommandToBeaconNavigation():
    xBee_compass.write()

#get signal strengths from the xbee
def getSignals():
    for i in range (0,9):
        xBee_serial = xBee_compass.readline()
        h, s = xBee_serial.split(",")
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
    #random direction seed
    make_drunk_walk(5, 3)
    #read bot compass
    botHeading = xBee_compass.readline()
    botHeading = int(botHeadings)
    botHeadings.append(botHeading)
    # print "botHeading"

    #find the avg bot compass reading
    botTotal = sum(botHeadings)
    botLength = len(botHeadings)
    avgBotHeading = botTotal / botLength
    print "avg bot heading: ", avgBotHeading

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
def findBeacon( bHeading):

    #	while(botHeading <= oppositeHeading or botHeading >= oppositeHeading):
    while (bHeading > cHeading + 4 and bHeading < cHeading - 4):
        botHeading = xBee_compass.readline()
<<<<<<< HEAD
        botHeading = float(botHeading)
        print botHeading
        rightRotate()
=======
        botHeading = int(botHeading)
        print(botHeading)
        rightRotate() #rotates until max(signalStrength)
>>>>>>> refs/remotes/origin/robot-py-luke

    findWay();

#Drunk Walk direction seed
def make_drunk_walk(step_size, step_count):
    move_options = (forward, leftTurn, rightTurn, reverse)
    for _ in range(step_count):
        move_somewhere = random.choice(move_options)
        move_somewhere(step_count)

#lidar obstacle avoidance
"""
def build_lidar(self):
    distanceArray = []

"""
def findWay(self):
    distanceArray = []

    # pan left
    lidar.panleft()
    time.sleep(1)
    distanceArray.append(lidar.distance())
    aux.writetofile('Pan Left Distace', distanceArray[0])

    # pan center
    lidar.pancenter()
    time.sleep(1)
    distanceArray.append(lidar.distance())
    aux.writetofile('Pan Center Distace', distanceArray[1])

    # pan right
    lidar.panright()
    time.sleep(1)
    distanceArray.append(lidar.distance())
    aux.writetofile('Pan Right Distace', distanceArray[2])


    maxdistance = max(distanceArray)
    maxindex = distanceArray.index(maxdistance)

    if maxindex == 0:
        leftRotate()
        aux.writetofile('Turning Left', distanceArray[maxindex])
    elif maxindex == 2:
        rightRotate()
        aux.writetofile('Turning Right', distanceArray[maxindex])
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
<<<<<<< HEAD
=======
    # TODO get new itr of sensor data from Arduino(s)

    #TODO detect goal position from compass, sigStr
    findHeading()

    #TODO: Augment goal data with sensor data

    #TODO: Send aug goal data to motor controll

>>>>>>> refs/remotes/origin/robot-py-luke
