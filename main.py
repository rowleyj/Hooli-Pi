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

#def getDist():
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
				counter= counter+1
				break
			else:
				sleep(1)
				GPS_Coords.append(GPSPing())
				
				
				
		
