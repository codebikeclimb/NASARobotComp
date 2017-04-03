#!/usr/bin/python
import serial

#initialize serial communications with XBee RF reciever
xBee = serial.Serial('/dev/ttyACM0',57600)

done = False
hL = []
sL = []

while not done:

   for i in range (0,9):		
	    xBee_serial = xBee.readline().strip()
	    h, s = xBee_serial.split(",")
            h = int(h)
	    s = int(s)
	    hL.append(h)
	    sL.append(s) 
  	    print sL
   done = True
