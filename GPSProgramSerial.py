from serial import *
from gps import *

#the usb port used for the gps is /dev/ttyACM0, baudrate = 4800
ser=Serial('/dev/ttyACM0',9600)
readText = ser.readline()
#print(ser)
print(readText)
newlist = readText.split(',')
print("newlist:",newlist)

ser.close()
