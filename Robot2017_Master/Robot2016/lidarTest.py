import serial
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import time
import math
import random
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
	for i in range(0,1000):
   		 leftFrontRear.setSpeed(70)
   		 rightFrontRear.setSpeed(70)
   		 rightFrontRear.run(Adafruit_MotorHAT.FORWARD)
   		 leftFrontRear.run(Adafruit_MotorHAT.BACKWARD)

def rightRotate():
   	for i in range(0,1000):
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
	time.sleep(0.5)
        a = random.randint(0,3)
	
	while(d <= 15):
	#	rightRotate()
			 turnOffMotors()
#		       	 d = getDistance()
		

	#	for i in range (1, (N)):
       			 if a == 0:
           			 rightRotate()
           			 print 'Rotating right'
                         	 d = getDistance()
				 print d
				 return d

			 if a == 1:
           			 leftRotate()
			         d = getDistance()
              			 print 'Rotating Left'
				 print d
				 return  d 

      			 if a == 2:
            			 reverse()
            			 print 'Backing dat ass up!'
        		
		
	turnOffMotors()
	time.sleep(0.5)
	forward()

#	move_choices = [rightRotate(), leftRotate(), reverse()]
#	for _ in range(step_count):
#		make_choice = random.choice(move_choices)
#		make_choice(step_count)
		
	



#	findWay()
#	done = True

atexit.register(turnOffMotors)


while not done:

	findWay()
		
