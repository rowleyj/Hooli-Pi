from gps import *
from time import *

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
		
print('my_position is: ', my_position)

#Need to decide best way to store data from all crashes, this is how we
#retreive the data, maybe consult with JR
