import RPi.GPIO
import serial
import time
import chardet
import sys

ser = serial.Serial('/dev/serial0', 921600, timeout = 2)

ser.write(bytearray.fromhex('57 10 FF FF 00 FF FF 63'))

while True:
	TOF_data=()
	
	
	if ser.in_waiting >= 6:
		print(ser.in_waiting)
		for i in range(0,ser.in_waiting):
			print(ord(ser.read(1)))
			#print(ser.read(1))
		
		ser.close()
		break

