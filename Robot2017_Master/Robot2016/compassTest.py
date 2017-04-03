import serial

compass = serial.Serial('/dev/ttyACM1', 9600)

done = False

cBearings = []

while not done:
	cSerial = compass.readline().strip()
        cSerial = int(cSerial)
        cBearings.append(cSerial)
        print cBearings


