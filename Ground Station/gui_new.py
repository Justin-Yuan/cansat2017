#import Tkinter
from serial import *
import ttk, user, sys, time, datetime, thread
from subprocess import check_output
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

from helpers import * 
from Aerial import * 
from UIelements import *

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

########################### Main Function ######################################

if __name__ == "__main__":
	# wirte header to log file  
	f = open(file_name, 'a')
	f.write("Team ID, Pack Cnt, Altitude, Pressure, Speed, Temp, Voltage, GPS Lat\
				GPS Long, GPS Alt, GPS Sat#, GPS Speed, Com Time, Com Cnt, State, Cam Angle\n")
	f.close()

	# initialize Cansat objects 
	container = Container()
	payload = Payload()

	# initialize the main gui
	root = MainGUI(None)
	root.title('CANSAT - 2017	Team: ' + str(TEAM_NUM))

	# initialize UI elements 
	panel = Panel(root)

	# Text Variables  
	text_var = TextVAr()

	# Top info bar 
	top_info_frame = TopInfoFrame(root, text_var)

	# Left info bar (team, time, flight status)
	left_info_frame = LeftInfoFrame(panel, text_var)

	# Force Button	 
	force_frame = ForceFrame(panel, text_var, force_status_var)
		
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
