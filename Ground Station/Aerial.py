from random import randint, uniform
import datetime

class Cansat(object):
	""" Cansat class to encapsulate shared variables and functions
	"""
	def __init__(self):
		self.packet_cnt = 0
		self.altitude = [0.0]
		self.mission_time = [str(datetime.datetime.now())[11:19]]
		self.pressure = [0.0]
		self.pitot = [0.0]
		self.temp_outside = [0.0]
		self.voltage = [0.0]
		self.heading = [0.0]
		self.gps_lat = [0.0]
		self.gps_long = [0.0]
		self.gps_alt = [0.0]
		self.gps_num = 0
		self.gps_speed = [0.0]

		self.flight_status = [0]

class Container(Cansat):
	"""
	"""
	def __init__(self):
		Cansat.__init__(self)


class Payload(Cansat):
	"""
	"""
	def __init__(self):
		Cansat.__init__(self)


class Telemetry(object):
	"""
	"""
	def __init__(self, target):
		self.ser = None
		self.ser_connected = False
		self.target = target

		# for testing wihtout serial only
		self.csv_test = True

	def serial_update_write(self, root, target):
		# for testing plots without serial connection only, delete this later
		if self.csv_test:
			altitude = randint(1, 400)
			pressure = randint(101, 120) #1
			pitot = randint(30,40) #2
			temp_outside = randint(22, 32) #3
			voltage = uniform(0, 8) #4
			gps_lat = randint(0, 100) #5
			gps_long = randint(0, 100) #6
			gps_alt = randint(0, 1000) #7
			gps_num = randint(0, 10) #8
			gps_speed = randint(30,40) #9
			com_cnt = randint(0,3) #10
			state = randint(1,7) #11
			angle = randint(-180,180) #12
			# heading?
			heading = randint(0,10) #idk
			target.packet_cnt += 1
			target.mission_time.append(str(datetime.datetime.now())[11:16])
			target.altitude.append(altitude)
			target.pressure.append(pressure)
			target.temp_outside.append(temp_outside)
			target.voltage.append(voltage)
			target.pitot.append(pitot)
			target.heading.append(heading)
			target.flight_status.append(state)


		elif self.ser_connected:
			data = self.ser.readline()
			data_list = data.split(",")
			#listbox.insert(0, ["TEST ",data_list])
			print data_list
			if len(data_list) == 8:
				#listbox.insert(0, ["TEST ",data_list])
				target.packet_cnt += 1
				for i in range(0,8):
					if (data_list[i] == ""):
						data_list[i] = str(000)

					try:
						float(data_list[i])
					except:
						data_list[i] = str(000)

				target.pitot.append(float(data_list[3]))
				target.altitude.append(float(data_list[4]))
				target.temp_outside.append(float(data_list[5]))
				target.voltage.append(float(data_list[6]))
				# need target.heading
				target.state = float(data_list[7])

		root.after(1000, self.serial_update_write, root, target)
