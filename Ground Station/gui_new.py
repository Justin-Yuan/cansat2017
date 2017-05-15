#import Tkinter
from serial import *
import ttk, user, sys, time, datetime, thread
from subprocess import check_output
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

try: 
	# for Python2
	import Tkinter as Tk 
except:
	# for Python3 
	import tkinter as Tk 


####################### Setup ########################################

# team information 
TEAM_NUM = 0000
baud_rate = 9600 
file_name = "cansat_2017.csv"

# initialize serial communication
global ser, ser_connected 
ser_connected = False 

# Vars
force_status_var = 0
packet_cnt = 0
last_com_time = 'N/A'

var_dict = {1:'data_altitude',2:'data_pressure',3:'data_pitot',4:'data_temp_outsi'}
flight_status_dict = {1:'Waiting', 2:'Ascending', 3:'Descending', 4:'Deploying',\
						5:'Gliding', 6:'Landed', 7:'Unknown'}

######################## Class Definitions ##################################

class Cansat(object):
	""" Cansat class to encapsulate shared variables and functions 
	"""
	def __init__(self, ):
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
		super().__init__(self, )


class Payload(Cansat):
	"""
	"""
	def __init__(self, ):
		super().__init__(self, )

		
class MenuBar(Tk.Menu):
	"""
	"""
	def __init__(self, parent):
		super().__init__(self, parent)


class StatusBar(Tk.Frame):
	"""
	"""
	def __init__(self, ):
		pass


class Chart(object):
	""" Chart class for data plots 
	"""
	def __init__(self, ):


	def plot_chart(self, type):
		global fig_temp, dataPlot_temp, a_temp

	    fig_temp = Figure(figsize=(4, 4), dpi = (frame.winfo_width() - 50) / 16)
	    dataPlot_temp = FigureCanvasTkAgg(fig_temp, master = chart2_frame)
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
	def __init__(self, parent):
		super().__init___(self, parent)

	def update_panel(self):
		pack_cnt.set("Packet Cnt: %d" % packet_cnt)
		pressure_var.set("Atm Pressure %.1f kPa" % data_pressure[-1])
		gps_lat.set("GPS Latitude: %.4f" % data_gps_lat[-1])
		gps_long.set("GPS Longitude: %.4f" % data_gps_long[-1])
		gps_num.set("GPS # Sat: %d" % data_gps_num)	
		com_cnt.set("Command Sent: %d" % data_com_cnt)
		cam_angle_text.set("Current Cam Angle: %d Degrees" % data_cam_angle)
		last_com.set("Last Cmd: %s" % last_com_time)
		root.after(1000, update_left_ribbon)	



############################## Function Definitions ################################

def serial_update_write():
	if ser_connected:
		data = ser.readline()
		data_list = data.split(",")
		#listbox.insert(0, ["TEST ",data_list])
		print data_list
		if len(data_list) == 13:
			#listbox.insert(0, ["TEST ",data_list])
			global packet_cnt, data_gps_num, data_state, data_cam_angle, data_com_cnt, last_com_time
			packet_cnt += 1
			for i in range(0,12):
				if (data_list[i] == ""):
					data_list[i] = str(000)

				try:
					float(data_list[i])
				except:
					data_list[i] = str(000)

			# update cam command time if snap received
			if data_com_cnt == float(data_list[10]) - 1:
				print 'Camera Snap Command Received'
				last_com_time = str(datetime.datetime.now())[0:19]
			data_com_cnt = float(data_list[10])
			write_str = ",".join([str(Team_Num),str(packet_cnt)] + data_list[0:9] + [str(data_com_cnt),str(last_com_time),str(data_list[11]),str(data_list[12])])
			listbox.insert(0, write_str)
			f = open(file_name, "a")
			f.write(write_str + "\n")
			f.close()

			data_altitude.append(float(data_list[0]))
			data_pressure.append(float(data_list[1]))
			data_pitot.append(float(data_list[2]))
			data_temp_outside.append(float(data_list[3]))
			data_voltage.append(float(data_list[4]))
			data_gps_lat.append(float(data_list[5]))
			data_gps_long.append(float(data_list[6]))
			data_gps_alt.append(float(data_list[7]))
			data_gps_num = float(data_list[8])
			data_gps_speed.append(float(data_list[9]))
			data_state = float(data_list[11])
			try:
				data_cam_angle = float(data_list[12])
			except:
				data_cam_angle = data_cam_angle

	root.after(500, ser_test_write)


def update_mission_time():
	current_time = str(datetime.datetime.now())[0: 19]
	mission_time.set("Mission Time: %s" % current_time)
	root.after(1000, update_mission_time)

def update_status():
	if ser_connected == 1:	   
		flight_status.set("Flight Status: " + flight_status_dict[data_state])
	else if ser_connected == 0:
		flight_status.set("Flight Status: Not Connected")
	else:
		flight_status.set("Flight Status: Unknown")
	root.after(200, update_flight_status)

def create_gui():
	pass

def create_label():
	pass

########################### Main Function ######################################

if __name__ == "__main__":
	# wirte header to log file  
	f = open(file_name, 'a')
	f.write("Team ID, Pack Cnt, Altitude, Pressure, Speed, Temp, Voltage, GPS Lat\
				GPS Long, GPS Alt, GPS Sat#, GPS Speed, Com Time, Com Cnt, State, Cam Angle\n")
	f.close()

	# initialize the main gui
	root = Tk.Tk() # create_gui()
	root.title('CANSAT - 2017	Team: ' + str(TEAM_NUM))

	# Text Variables  
	mission_time = Tk.StringVar()

	force_status = Tk.StringVar()
	force_status.set("None Selected")

	flight_status = Tk.StringVar()
	flight_status.set("Flight Status: Not Connected")

	pack_cnt = Tk.StringVar()
	pack_cnt.set("Packet Cnt: %d" % packet_cnt)

	pressure_var = Tk.StringVar()
	pressure_var.set("Atm Pressure %d kPa" % data_pressure[-1])

	gps_lat = Tk.StringVar()
	gps_lat.set("GPS Latitude: %d" % float(data_gps_lat[-1]))

	gps_long = Tk.StringVar()
	gps_long.set("GPS Longitude: %d" % float(data_gps_long[-1]))

	gps_num = Tk.StringVar()
	gps_num.set("GPS # Sat: %d" % data_gps_num)

	com_cnt = Tk.StringVar()
	com_cnt.set("Command Sent: %d" % data_com_cnt)

	last_com = Tk.StringVar()
	last_com.set("Last Cmd: %s" % last_com_time)

	cam_angle_text = Tk.StringVar()
	cam_angle_text.set("Current Cam Angle: %d Degrees" % data_cam_angle)
	cam_angle_entry = Tk.StringVar()

	# Top info bar 
	top_info_frame = Tk.Frame(root, bg='black')
	top_info_frame.pack(side = "top", expand = 1, fill = 'x')
	
	label_top1 = Tk.Label(top_info_frame, text = "TEAM #"+str(TEAM_NUM), fg='white', bg='black')
	label_top1.pack(side='left', expand = 1, fill = 'x')

	mission_time.set("Mission Time: %s" % str(datetime.datetime.now())[0:19])
	label_top2 = Tkinter.Label(top_info_frame, textvariable = mission_time, fg='white', bg='black')
	label_top2.pack(side='left', expand = 1, fill = 'x')

	label_top3 = Tk.Label(top_info_frame, textvariable = flight_status,fg='white', bg='black') 
	label_top3.pack(side='left', expand = 1, fill = 'x')

	# left ribbon
	left_ribbon = Tk.Frame(root)
	left_ribbon.pack(side = "left", expand = 1, padx = 20, fill = 'y')

	# other info bar (team, time, flight status)
	info_frame = Tk.Frame(left_ribbon)
	info_frame.pack(side = "top",expand = 1,  fill = 'both')

	label_info0 = Tk.Label(info_frame, textvariable = pack_cnt )
	label_info0.grid(column = 0, row = 0,sticky = 'w')

	label_info4 = Tk.Label(info_frame, textvariable = pressure_var )
	label_info4.grid(column = 0, row = 1,sticky = 'w')

	label_info1 = Tk.Label(info_frame, textvariable = gps_lat)
	label_info1.grid(column = 0, row = 2,sticky = 'w')

	label_info2 = Tk.Label(info_frame, textvariable = gps_long)
	label_info2.grid(column = 0, row = 3,sticky = 'w')

	label_info3 = Tk.Label(info_frame, textvariable = gps_num)
	label_info3.grid(column = 0, row = 4,sticky = 'w')

	# Force Button	 
	status_button_frame = Tk.Frame(left_ribbon, bg = 'red')
	status_button_frame.pack(side = "top", expand = 1, fill = 'both')

	label_force = Tk.Label(status_button_frame, text = "FORCE ACTIONS",bg = 'red')
	label_force.pack(side = 'top', fill = 'both')

	button_none = Tk.Button(status_button_frame,text=u"None",command = lambda x=0: force_status_callback(x))
	button_none.pack(side = 'top')

	button_deploy = Tk.Button(status_button_frame,text=u"Deploy",command = lambda x=1: force_status_callback(x))
	button_deploy.pack(side = 'top')

	button_land = Tk.Button(status_button_frame,text=u"Land",command = lambda x=2: force_status_callback(x))
	button_land.pack(side = 'top')

	label_force_status = Tk.Label(status_button_frame, textvariable = force_status ,pady=12, bg = 'red')
	label_force_status.pack(side = 'top',fill = 'x')

	button_act = Tk.Button(status_button_frame, text = "Execute",command = execute_button_callback)
	button_act.pack(side = 'top')
		
	# Main chart area
	frame = Tk.Frame(root)
	frame.pack(side='top', expand = 1, fill='x')
	frame.bind("<Key>", key)
	frame.focus_set()

	chart1_frame = Tk.Frame(frame)
	chart1_frame.pack(side = "left", expand = 1, fill = 'both')

	chart2_frame = Tk.Frame(frame)
	chart2_frame.pack(side = "left", expand = 1, fill = 'both')

	chart3_frame = Tk.Frame(frame)
	chart3_frame.pack(side = "left", expand = 1, fill = 'both')

	chart4_frame = Tk.Frame(frame)
	chart4_frame.pack(side = "left", expand = 1, fill = 'both')

	# Scroll Telemetry
	stream_frame = Tk.Frame(root, bg = "white")
	stream_frame.pack(side = "top", pady = 0, fill = 'both', expand = True)

	scrollbar = Tk.Scrollbar(stream_frame)
	scrollbar.pack(side = 'right', fill = 'y')

	listbox = Tk.Listbox(stream_frame, width = 600,height = 20, yscrollcommand=scrollbar.set)
	listbox.pack(side ='left', fill = 'both')
	scrollbar.config(command=listbox.yview)
	

	# Bottom status bar
	status = StatusBar(root)
	status.pack(side='bottom', fill='x') 
	
 	
 	# call loops 
 	root.after(0, plot_altitude)
 	root.after(0, plot_temperature)
	root.after(0, plot_pitot)
	root.after(0, plot_voltage)

	root.after(0, update_mission_time)
	root.after(0, update_flight_status)
	root.after(0, update_left_ribbon)
	root.after(1000, ser_test_write)
	root.after(1000, conclude)

	root.mainloop()
