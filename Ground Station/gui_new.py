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
TEAM_NUM = 6159
baud_rate = 9600
file_name = "cansat_2017.csv"

# initialize serial communication
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
	f = open(file_name, 'aw+')
	f.write("6159,GLIDER,MISSION_TIME,PACKET_CNT,ALTITUDE,PRESSURE,SPEED,TEMP,VOLTAGE,HEADING,SOFTWARE_STATE\n")
	f.close()
	# initialize Cansat objects
	container = Container()
	payload = Payload()
	tel = Telemetry(container)
	# target viraible holds the current object being monitored
	target = container


	# initialize the main gui
	root = MainGUI(None, container)
	root.title('CANSAT - 2017	Team: ' + str(TEAM_NUM))

	# initialize UI elements
	panel = Panel(root, container, payload)

	# Text Variables
	text_var = TextVar(container)

	# Top info bar
	top_info_frame = TopInfoFrame(root, text_var, TEAM_NUM)

	# Left info bar (team, time, flight status)
	left_info_frame = LeftInfoFrame(panel, text_var)

	# Force Button
	force_frame = ForceFrame(panel, text_var, force_status_var, tel)

	# Main chart area
	chart = Chart(root, container, payload)

	# Scroll Telemetry
	telemetry_box = TelemetryBox(root)

	# Bottom status bar
	status = StatusBar(root)
	status.pack(side='bottom', fill='x')


 	# call loops
 	root.after(0, chart.plot_altitude, target)
 	root.after(0, chart.plot_temperature, target)
	root.after(0, chart.plot_pitot, target)
	root.after(0, chart.plot_voltage, target)

	root.after(0, update_mission_time, text_var, root)
	root.after(0, update_flight_status, tel, text_var, root)
	root.after(0, panel.update_panel, root, target, text_var)
	root.after(1000, tel.serial_update_write, root, target)
	root.after(1000, conclude, chart)

	root.after(500, check_target, container, payload, target)

	root.mainloop()
