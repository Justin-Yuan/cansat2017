try: 
	# for Python2
	import Tkinter as Tk 
except:
	# for Python3 
	import tkinter as Tk 

class MainGUI(Tk.Tk):
	def __init__(self,parent):
		Tk.Tk.__init__(self,parent)
		self.parent = parent
		self.geometry("1200x1000+ 100+50")
		self.config(menu=MenuBar(self))

		
class MenuBar(Tk.Menu):
	"""
	"""
	def __init__(self, parent):
		super().__init__(self, parent)
		self.parent = parent 
		self.initialize()

	def initialize(self):
		# File menu 
	    file_menu = Tk.Menu(self, tearoff=0)
		file_menu.add_command(label="Save", command=self.save_data)
		file_menu.add_separator()
		file_menu.add_command(label="Start", command=self.start_operation)
		file_menu.add_command(label="Pause", comamnd=self.pause_operation)
		file_menu.add_command(label="Stop", command=self.stop_operation)
		file_menu.add_separator()		
		file_menu.add_command(label="Exit", underline=1, command=self.quit)
		self.add_cascade(label="File", underline=0, menu=file_menu)

		# Connection menu 
		port_menu = Tk.Menu(self, tearoff=0)
		found_port = False 
		for port in check_output(["ls", "/dev"]).split("\n"):
			if port.find("USB") != -1:
				found_port = True
				usb_port = str(port)
				print(usb_port)
				port_menu.add_command(label=port, command=lambda usb_port=usb_port: self.open_ser(usb_port))

		port_menu.add_command(label="Disconnect", command=self.disconnect)				

		if not found_port:
			port_menu.add_command(label="No COM Device Found")

		self.add_cascade(label="Connection", underline=0, menu=port_menu)

		# Help menu 
		help_menu = Tk.Menu(self, tearoff=0)
		help_menu.add_command(label="About", command=self.info)
		self.add_cascade(label="Help", menu=help_menu)

	def save_data(self):
		pass 

	def start_operation(self):
		pass 

	def pause_operation(self):
		pass 

	def stop_operation(self):
		pass 

	def quit(self):
		sys.exit(0)

	def open_ser(self, usb_port):
		global ser, ser_connected
		address = "/dev/" + usb_port
		try:
			ser = Serial(address, baud_rate, timeout=0, writeTimeout=0)
			# TODO what is status ? 
			status.set("Connected to %s" % usb_port)
			ser_connected = True 
			print("Connected to " + usb_port)
			flight_status.set("Flight Status: Ready")
		except Exception as e:
			print("Error:connection cannot be established")
			root.status.set("Error: connection cannot be established. %s" % e)

	def disconnect(self, usb_port):
		global ser, ser_connected
		ser.close()
		ser_connected = False 
		print("Ended connection")
		flight_status.set("Flight Status: Standby")


class StatusBar(Tk.Frame):
	"""
	"""
	def __init__(self, parent):
		super().__init__(self, parent)
		self.label = Tk.Label(self, relief='sunken', anchor='w')
		self.label.pack(fill='x')
		self.set("CANSAT-2017 with RSX")

	def set(self, format, *args):
		self.label.config(text=format % args)
		self.label.update_idletasks()

	def clear(self):
		self.label.set("")


class Chart(object):
	""" Chart class for data plots 
	"""
	def __init__(self, parent, containter, payload):
		self.container = container 
		self.payload = payload 

		self.frame = Tk.Frame(parent)
		self.chart1_frame = Tk.Frame(self.frame)
		self.chart2_frame = Tk.Frame(self.frame)
		self.chart3_frame = Tk.Frame(self.frame)
		self.chart4_frame = Tk.Frame(self.frame)

	def pack_frame(self):
		self.frame.pack(side='top', expand = 1, fill='x')
		self.frame.bind("<Key>", self.key)
		self.frame.focus_set()

		self.chart1_frame.pack(side = "left", expand = 1, fill = 'both')
		self.chart2_frame.pack(side = "left", expand = 1, fill = 'both')
		self.chart3_frame.pack(side = "left", expand = 1, fill = 'both')
		self.chart4_frame.pack(side = "left", expand = 1, fill = 'both')

	def key(self, event):
		return
#    root.status.set(repr(event.char)) 

	def plot_altitude():
	    global fig_altitude, dataPlot_altitude, a_altitude

	    fig_altitude = Figure(figsize=(4, 4), dpi = (frame.winfo_width() - 50) / 16)
	    dataPlot_altitude = FigureCanvasTkAgg(fig_altitude, master = self.chart1_frame)
	    a_altitude = fig_altitude.add_subplot(111)

	    dataPlot_altitude.show()
	    dataPlot_altitude.get_tk_widget().pack()

	    def plot_cts(target):
	        global a_altitude

	        if target == "container":
		        x_axis1 = range(0, len(self.container.altitude))
		        x_axis2 = range(0, len(self.container.gps_alt))

		        a_altitude.clear()
		        a_altitude.plot(x_axis1, self.container.altitude, "r", label = "BMP180")
				a_altitude.plot(x_axis2, self.container.gps_alt, "b", label = "GPS")
			elif target == "payload":
				x_axis1 = range(0, len(self.payload.altitude))
		        x_axis2 = range(0, len(self.payload.gps_alt))

		        a_altitude.clear()
		        a_altitude.plot(x_axis1, self.payload.altitude, "r", label = "BMP180")
				a_altitude.plot(x_axis2, self.payload.gps_alt, "b", label = "GPS")
	        
	        a_altitude.set_title("Altitude (m)")
			legend = a_altitude.legend(loc='upper left', shadow=True)       

	        dataPlot_altitude.show()
	        dataPlot_altitude.get_tk_widget().pack()

	        root.after(1000, plot_cts)

	    plot_cts()

	def plot_chart(self, type):
		global fig_temp, dataPlot_temp, a_temp

	    fig_temp = Figure(figsize=(4, 4), dpi = (frame.winfo_width() - 50) / 16)
	    dataPlot_temp = FigureCanvasTkAgg(fig_temp, master = self.chart2_frame)
	    a_temp = fig_temp.add_subplot(111)

	    dataPlot_temp.show()
	    dataPlot_temp.get_tk_widget().pack()

		def plot_cts():
		    global a_temp
		    x_axis = range(0, len(data_temp_outside))

		    a_temp.clear()
		    a_temp.plot(x_axis, data_temp_outside, "r", label = "Outside")

		    a_temp.set_title("Temperature (C)")
		    a_temp.set_ylim([0, 60])

		    dataPlot_temp.show()
		    dataPlot_temp.get_tk_widget().pack() 

		    root.after(1000, plot_cts)

	    plot_cts()    


class Panel(Tk.Frame):
	""" Panel for showing current data 
	"""
	def __init__(self, parent, container, payload):
		super().__init___(self, parent)
		self.pack(side = "left", expand = 1, padx = 20, fill = 'y')

		self.container = container
		self.payload = payload 

# TODO need to add a target here: whether it's container or payload 
	def update_panel(self):
		pack_cnt.set("Packet Cnt: %d" % packet_cnt)
		pressure_var.set("Atm Pressure %.1f kPa" % data_pressure[-1])
		gps_lat.set("GPS Latitude: %.4f" % data_gps_lat[-1])
		gps_long.set("GPS Longitude: %.4f" % data_gps_long[-1])
		gps_num.set("GPS # Sat: %d" % data_gps_num)	
		com_cnt.set("Command Sent: %d" % data_com_cnt)
		cam_angle_text.set("Current Cam Angle: %d Degrees" % data_cam_angle)
		last_com.set("Last Cmd: %s" % last_com_time)
		root.after(1000, update_panel)	


class TextVar(object):
	"""
	"""
	def __init__(self):
		self.mission_time = Tk.StringVar()
		self.force_status = Tk.StringVar()
		self.flight_status = Tk.StringVar()
		self.pack_cnt = Tk.StringVar()
		self.pressure_var = Tk.StringVar()
		self.gps_lat = Tk.StringVar()
		self.gps_long = Tk.StringVar()
		self.gps_num = Tk.StringVar()

		set_text()

	def set_text(self):
		self.force_status.set("None Selected")
		self.flight_status.set("Flight Status: Not Connected")
		self.pack_cnt.set("Packet Cnt: %d" % packet_cnt)
		self.pressure_var.set("Atm Pressure %d kPa" % data_pressure[-1])
		self.gps_lat.set("GPS Latitude: %d" % float(data_gps_lat[-1]))
		self.gps_lat.set("GPS Latitude: %d" % float(data_gps_lat[-1]))
		self.gps_long.set("GPS Longitude: %d" % float(data_gps_long[-1]))
		self.gps_long.set("GPS Longitude: %d" % float(data_gps_long[-1]))
		self.gps_num.set("GPS # Sat: %d" % data_gps_num)


class TopInfoFrame(TK.Frame):
	"""
	"""
	def __init__(self, parent, text_var):
		self.top_info_frame = Tk.Frame(parent, bg='black')	
		# TODO change TEAM_NUM	
		self.label_top1 = Tk.Label(self.top_info_frame, text = "TEAM #"+str(TEAM_NUM), fg='white', bg='black')
		self.label_top2 = Tk.Label(self.top_info_frame, textvariable = text_var.mission_time, fg='white', bg='black')
		self.label_top3 = Tk.Label(self.top_info_frame, textvariable = text_var.flight_status, fg='white', bg='black') 

		self.pack_frame()		

	def pack_frame(self):
		self.top_info_frame.pack(side = "top", expand = 1, fill = 'x')
		self.label_top1.pack(side='left', expand = 1, fill = 'x')
		self.label_top2.pack(side='left', expand = 1, fill = 'x')
		self.label_top3.pack(side='left', expand = 1, fill = 'x')


class LeftInfoFrame(Tk.Frame):
	"""
	"""
	def __init__(self, parent, text_var):
		self.info_frame = Tk.Frame(parent)
		self.label_info0 = Tk.Label(self.info_frame, textvariable = text_var.pack_cnt)
		self.label_info4 = Tk.Label(self.info_frame, textvariable = text_var.pressure_var)
		self.label_info1 = Tk.Label(self.info_frame, textvariable = text_var.gps_lat)
		self.label_info2 = Tk.Label(self.info_frame, textvariable = text_var.gps_long)
		self.label_info3 = Tk.Label(self.info_frame, textvariable = text_var.gps_num)

		self.pack_frame()

	def pack_frame(self):
		self.info_frame.pack(side = "top",expand = 1,  fill = 'both')
		self.label_info0.grid(column = 0, row = 0,sticky = 'w')
		self.label_info4.grid(column = 0, row = 1,sticky = 'w')
		self.label_info1.grid(column = 0, row = 2,sticky = 'w')
		self.label_info2.grid(column = 0, row = 3,sticky = 'w')
		self.label_info3.grid(column = 0, row = 4,sticky = 'w')


class ForceFrame(Tk.Frame):
	"""
	"""
	def __init__(self, parent, text_var, force_status_var):
		self.force_status_var = force_status_var
		self.status_button_frame = Tk.Frame(parent, bg = 'red')
		self.label_force = Tk.Label(self.status_button_frame, text = "FORCE ACTIONS",bg = 'red')

		self.button_none = Tk.Button(self.status_button_frame,text=u"None",command = lambda x=0: self.force_status_callback(x, self.force_status_var))
		self.button_deploy = Tk.Button(self.status_button_frame,text=u"Deploy",command = lambda x=1: self.force_status_callback(x, self.force_status_var))
		self.button_land = Tk.Button(self.status_button_frame,text=u"Land",command = lambda x=2: self.force_status_callback(x, self.force_status_var))
		self.label_force_status = Tk.Label(self.status_button_frame, textvariable = text_var.force_status ,pady=12, bg = 'red')
		self.button_act = Tk.Button(self.status_button_frame, text = "Execute",command = self.execute_button_callback)

		self.pack_frame()

	def pack_frame(self):
		self.status_button_frame.pack(side = "top", expand = 1, fill = 'both')
		self.label_force.pack(side = 'top', fill = 'both')
		self.button_none.pack(side = 'top')
		self.button_deploy.pack(side = 'top')
		self.button_land.pack(side = 'top')
		self.label_force_status.pack(side = 'top',fill = 'x')
		self.button_act.pack(side = 'top')

# TODO status and force_status variables 
	def force_status_callback(self, status, force_status_var):
		if status == 1:
			force_status.set("Deploy Selected")
			force_status_var = 1
		elif status == 2:
			force_status.set("Land Selected")
			force_status_var = 2
		else:
			force_status.set("None Selected")
			force_status_var = 0

# TODO ser_connected variable and ser variable 
	def execute_button_callback(self, ser_connected, ser):
		try:
			if ser_connected == 1:
				if force_status_var == 1 or force_status_var == 2:
					ser.write('f %d\n' % force_status_var)
					print 'force command sent with %d' % force_status_var
				else:
					print 'Nothing was executed'
		except Exception as e:
			print "Error: Could not write to serial"
			# ????
	    		root.status.set("Error: Could not write to serial. %s" % e)


class TelemetryBox(Tk.Frame):
	"""
	"""
	def __init__(self, parent):
		self.stream_frame = Tk.Frame(parent, bg = "white")
		self.scrollbar = Tk.Scrollbar(self.stream_frame)
		self.listbox = Tk.Listbox(self.stream_frame, width = 600,height = 20, yscrollcommand=self.scrollbar.set)

		self.pack_frame()

	def pack_frame(self):
		self.stream_frame.pack(side = "top", pady = 0, fill = 'both', expand = True)
		self.scrollbar.pack(side = 'right', fill = 'y')
		self.listbox.pack(side ='left', fill = 'both')
		self.scrollbar.config(command=self.listbox.yview)
