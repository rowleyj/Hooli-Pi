import RPi.GPIO
import serial
import time
import chardet
import sys

ser = serial.Serial('/dev/serial0', 921600, timeout = 2)


# while True:
# 	TOF_data=()
	
	
# 	if ser.in_waiting >= 6:
# 		print(ser.in_waiting)
# 		for i in range(0,ser.in_waiting):
# 			print(ord(ser.read(1)))
# 			#print(ser.read(1))
		
# 		ser.close()
# 		break

writeToId = [ '00', '00', '00']
checkSum = ['63', '63', '63']
idx = 0

while True:
	print('top of loop', 'writing to: '+writeToId[idx])
	print(bytearray(b'5710FFFF'+writeToId[idx]+'FFFF'+checkSum[idx], 'utf-8')) 
	ser.reset_input_buffer()
	ser.write(bytearray.fromhex('57 10 FF FF '+writeToId[idx]+' FF FF '+checkSum[idx]))

	while(ser.in_waiting < 6): 
		time.sleep(0.5) 
		print('waiting...', writeToId[idx], checkSum[idx], ser.in_waiting)

	if ser.in_waiting >= 6:
		for i in range(0, ser.in_waiting):
			print(ord(ser.read(1)))

	# alter id to write to next in queue
	idx = idx + 1
	if(idx > len(writeToId)): idx = 0
