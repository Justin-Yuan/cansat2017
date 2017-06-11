# test code to send dummy values over serial

from serial import *
import datetime, time
from random import randint

serialPort = "/dev/ttyUSB0"
baudRate = 9600
ser = Serial(serialPort , baudRate, timeout=0, writeTimeout=0)
pack_cnt = 0;

# TEAM_ID,MISSION_TIME,ALT_SENSOR,OUTSIDE_TEMP,INSIDE_TEMP,VOLTAGE,FSW_STATE,ACC_X,ACC_Y,ACC_Z

while True:
	pack_cnt += 1 #;

	altitude = 'nan'
	pressure = randint(101, 120) #1
	pitot = randint(30,40) #2
	temp_outside = randint(22, 32) #3
	voltage = randint(5, 8) #4
	gps_lat = randint(0, 100) #5
	gps_long = randint(0, 100) #6
	gps_alt = randint(0, 1000) #7
	gps_num = randint(0, 10) #8
	gps_speed = randint(30,40) #9
	com_cnt = randint(0,3) #10
	state = randint(0,7) #11
	angle = randint(-180,180) #12

	# todo: writes the bytes data to the port, but seriously where does it write to ?
	ser.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (altitude, pressure, pitot, temp_outside, voltage, gps_lat, gps_long, gps_alt, gps_num,gps_speed,com_cnt,state,angle))

	time.sleep(1)
