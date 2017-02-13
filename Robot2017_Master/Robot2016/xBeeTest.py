#!/usr/bin/python
import serial

#initialize serial communications with XBee RF reciever
xBee = serial.Serial('/dev/ttyACM0',57600)

done = False
hL = []
sL = []

while not done:
    xBee_serial = xBee.readline()
    h, s = xBee_serial.split(",")
    hL.append(h)
    sL.append(s) 
    print sL
