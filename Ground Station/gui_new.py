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
	panel = Panel(root, container, payload)

	# Text Variables  
	text_var = TextVAr()

	# Top info bar 
	top_info_frame = TopInfoFrame(root, text_var)

	# Left info bar (team, time, flight status)
	left_info_frame = LeftInfoFrame(panel, text_var)

	# Force Button	 
	force_frame = ForceFrame(panel, text_var, force_status_var)
		
	# Main chart area
	chart = Chart(root, container, payload)

	# Scroll Telemetry
	telemetry_box = TelemetryBox(root)
	
	# Bottom status bar
	status = StatusBar(root)
	status.pack(side='bottom', fill='x') 
	
 	
 	# call loops 
 	root.after(0, chart.plot_altitude)
 	root.after(0, chart.plot_temperature)
	root.after(0, chart.plot_pitot)
	root.after(0, chart.plot_voltage)

	root.after(0, update_mission_time, text_var, root)
	root.after(0, update_flight_status, ser_connected, text_var, root)
	root.after(0, panel.update_panel)
	root.after(1000, serial_update_write)
	root.after(1000, conclude, frame)

	root.mainloop()
