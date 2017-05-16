class Cansat(object):
	""" Cansat class to encapsulate shared variables and functions 
	"""
	def __init__(self):
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
		
		self.com_cnt = 0
		self.state = 0
		self.cam_angle = 0


class Container(Cansat):
	""" 
	"""
	def __init__(self, ):
		super().__init__(self)


class Payload(Cansat):
	"""
	"""
	def __init__(self, ):
		super().__init__(self)