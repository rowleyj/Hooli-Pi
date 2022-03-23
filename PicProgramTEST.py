from picamera import PiCamera
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN)
camera = PiCamera()

count =0


while True:
	if GPIO.input(24) == 1:
		camera.start_preview()
		time.sleep(5)
		count = count+1
		camera.capture('/home/pi/Desktop/Payload/Recordings/testpic'+str(count)+'.jpg')
		camera.stop_preview()
		print('program halted, vvideo recorded')



