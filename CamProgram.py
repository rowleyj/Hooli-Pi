from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN)
camera = PiCamera()


camera.start_preview()
camera.start_recording('/home/pi/Desktop/Payload/Recordings/testvid.h264')
while True:
	if GPIO.input(24) == 1:
		camera.stop_recording()
		camera.stop_preview()
		print('program halted, vvideo recorded')



