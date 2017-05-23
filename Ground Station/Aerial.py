class Cansat(object):
	""" Cansat class to encapsulate shared variables and functions
	"""
	def __init__(self):
		self.packet_cnt = 0

		self.altitude = [0.0]
		self.pressure = [0.0]
		self.pitot = [0.0]
		self.temp_outside = [0.0]
		self.voltage = [0.0]

		self.gps_lat = [0.0]
		self.gps_long = [0.0]
		self.gps_alt = [0.0]
		self.gps_num = 0
		self.gps_speed = [0.0]


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

	def serial_update_write(self, root, target):
		if self.ser_connected:
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


				target.altitude.append(float(data_list[4]))
				target.temp_outside.append(float(data_list[5]))
				target.voltage.append(float(data_list[6]))
				target.state = float(data_list[7])

		root.after(500, self.serial_update_write, root, target)
