#import libraries
from gps import *
from time import *
import serial
import chardet
import sys
from picamera import PiCamera
import RPi.GPIO as GPIO
import subprocess
import json


#psuedocode
#while true (This program runs while the pi is on)
	#press button to begin data recording session
		#record start time (epoch time)
		#start camera recording
		#start recording distance sensor data on x sec loop
		#also record gps data on x sec loop
		
		
		#when distance sensors are less than 1m, get time of pass and store
		
		#press button, stop recording video, stop recording data
		#convert video format to mp4
		#package sensor data arrays into json file
		
	#NOTE probably do button off by having if statement each loop if button is off record data
	#if button is on stop data and leave teh inner loop 
#function definitions
#Defining constant variables
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN)
GPIO.setup(23, GPIO.OUT)
camera = PiCamera()
camera.resolution = (1920,1080)
#Defining GPS Ping function, gets current position
def GPSPing():
	#Listen to port 2947
	#2947 is port gpsd communicates on
	my_gps = gps("localhost","2947")
	my_gps.stream(WATCH_ENABLE | WATCH_NEWSTYLE)
	my_position = []

	#Wait for gps info
	while True:
		try:
			
			report = my_gps.next()
			#wait for an input and then store coordinates
			
			if report['class'] == 'TPV':
				if hasattr(report, 'lon'):
					
					my_position.append(report.lon)
				if hasattr(report, 'lat'):
					my_position.append(report.lat)
					
				
				break
		except KeyError:
			pass
		except KeyboardInterrupt:
			break
			
	return my_position
	
#Defining Distance Sensor Ping function
#Gets readings from all 3 sensors, outputs array of 3 readings
TOF_length = 16
TOF_header = (87, 0, 255)
TOF_distance = 0

ser = serial.Serial('/dev/serial0', 115200, timeout=2.0)
ser.reset_input_buffer()
def verifyCheckSum(data,length):
	TOF_check =0
	print(data)
	print(length)
	print("length:",len(data))
	for k in range(0, length-1):
		TOF_check += data[k]
	TOF_check = TOF_check%256
	
	if(TOF_check == data[length-1]):
		#data is ok
		return 1
	else:
		#data is not okay, error present
		return 0
def getDist():
	ser.reset_input_buffer()
	while True:
	TOF_data=()
	sleep(0.05)
	
	try:
		
		#print("Type test", type(ser.in_waiting()))
		if ser.in_waiting >= 32:
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
						return TOF_distance
						break
			break
	except:
		print("Excepterino")
		ser = serial.Serial('/dev/serial0', 115200, timeout=2.0)
		ser.reset_input_buffer()
#	#loop distance sensor code
#	distances =[]
	
	
#	return distances
counter= 0
while True:
	
	#User pushes record button, start record loop
	if GPIO.input(24) == 1:
		print("Starting Ride...")
		#sleep so we don't immediately terminate program
		sleep(5)
		GPIO.output(23,1)
		print("Ride Successfully Started!")
		#start camera recording
		camera.start_preview()
		camera.start_recording('/home/pi/Desktop/Payload/Recordings/testvid'+str(counter)+'.h264')
		
		startTime = time()
		#initialize data arrays to be packaged into json file
		GPS_Coords = []
		miss_times = []
		#user pushes record button, save data and exit record loop
		while True:
			
			if GPIO.input(24) == 1:
				camera.stop_recording()
				camera.stop_preview()
				
				
				#print('program halted, vvideo recorded')
				endTime = time()
				#package data
				command = "MP4Box -add /home/pi/Desktop/Payload/Recordings/testvid"+str(counter)+".h264 /home/pi/Desktop/Payload/Recordings/testvid"+str(counter)+".mp4"
				subprocess.call([command], shell=True)
				myPackage = {"start":startTime, "end":endTime, "GPS":GPS_Coords, "misses":miss_times}
				pkgString = json.dumps(myPackage)
				jsonFile = open("/home/pi/Desktop/Payload/payload.json", "w")
				jsonFile.write(pkgString)
				jsonFile.close()
				print("Saving Data...")
				#sleep so we don't immediately start the program
				sleep(5)
				print("Ride Ended")
				GPIO.output(23,0)
				counter= counter+1
				break
			else:
				sleep(1)
				GPS_Coords.append(GPSPing())
				sense_dist = getDist()
				if sense_dist<=1000:
					miss_time.append(time())
				
				
				
		
