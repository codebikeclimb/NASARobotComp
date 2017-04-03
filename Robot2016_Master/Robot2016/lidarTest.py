import serial
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import time
import atexit


lidar = serial.Serial('/dev/ttyACM1', 115200)

done = False


roboMotor = Adafruit_MotorHAT(addr=0x60)

#create motor objects
leftFrontRear = roboMotor.getMotor(1)
rightFrontRear = roboMotor.getMotor(3)

#motor functions
########################################################################################################################
# drive forwards
def forward():
#    print "forward!"
    leftFrontRear.setSpeed(80)
    rightFrontRear.setSpeed(80)
    leftFrontRear.run(Adafruit_MotorHAT.FORWARD)
    rightFrontRear.run(Adafruit_MotorHAT.FORWARD)


# drive backwards
def reverse():
#    print "reverse!"
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
	roboMotor.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	roboMotor.getMotor(3).run(Adafruit_MotorHAT.RELEASE)




def getDistance():
	
#	global distance 	

	lidar_serial = lidar.readline().strip().lstrip('WIN!')
	if(lidar_serial != 'nack' and lidar_serial != 'NACK' and lidar_serial != '> nack' and lidar_serial != 'ACK' and lidar_serial != ''):
		lidar_serial = int(lidar_serial)
	print lidar_serial

	return lidar_serial




def findWay():
#	global distance        
	d = getDistance()
	while(d > 15):
		forward()
		d = getDistance()

	
	turnOffMotors()
	delay(150)
	while(d <= 15):
		rightRotate()
		d = getDistance()
		
	turnOffMotors()
	delay(150)
	forward()



#	findWay()
#	done = True

atexit.register(turnOffMotors)


while not done:

	findWay()
		
