import RPi.GPIO
import serial
import time
import chardet
import sys

TOF_length = 16
TOF_header = (87, 0, 255)
TOF_distance = 0

ser = serial.Serial('/dev/serial0', 921600, timeout=2.0)
ser.reset_input_buffer()

#Checksum used in while loop to check data is error free

def verifyCheckSum(data,len):
	TOF_check =0
	for k in range(0, len-1):
		TOF_check += data[k]
	TOF_check = TOF_check%256
	
	if(TOF_check == data[len-1]):
		#data is ok
		return 1
	else:
		#data is not okay, error present
		return 0

while True:
	TOF_data=()
	time.sleep(0.05)
	print("Type test", type(ser.in_waiting()))
	if ser.in_waiting() >= 32:
		for i in range(0,16):
			TOF_data = TOF_data + (ord(ser.read(1)), ord(ser.read(1)))
		print("TOF_data:", TOF_data)
		
		for j in range(0,16):
			if((TOF_data[j]==TOF_header[0] and TOF_data[j+1] == TOF_header[1] and TOF_data[j+2]==TOF_header[2]) and (verifyCheckSum(TOF_data[j:TOF_length],TOF_length))):
				if(((TOF_data[j+12]) | (TOF_data[j+13]<<8))==0):
					#it's out of range
					print("out of range")
				else:
					print("id is:", TOF_data[j+3])
					
					TOF_distance = (TOF_data[j+8]) | (TOF_data[j+9]<<8) | (TOF_data[j+10]<<16);
					print("Distance is:", TOF_distance)
		
