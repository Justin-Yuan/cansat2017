import ttk, user, sys, time, datetime, thread
from Aerial import *

var_dict = {1:'data_altitude',2:'data_pressure',3:'data_pitot',4:'data_temp_outsi'}
flight_status_dict = {1:'Waiting', 2:'Ascending', 3:'Descending', 4:'Deploying',\
						5:'Gliding', 6:'Landed', 7:'Unknown'}

def update_mission_time(text_var, root):
	current_time = str(datetime.datetime.now())[0: 19]
	text_var.mission_time.set("Mission Time: %s" % current_time)
	root.after(1000, update_mission_time, text_var, root)

def update_flight_status(tel, text_var, root):
	if tel.ser_connected == True:
		text_var.flight_status.set("Flight Status: " + flight_status_dict[data_state])
	elif tel.ser_connected == False:
		text_var.flight_status.set("Flight Status: Not Connected")
	else:
		text_var.flight_status.set("Flight Status: Unknown")

	root.after(200, update_flight_status, tel, text_var, root)

def conclude(chart):
    chart.frame.focus_set()

def check_target(container, payload, target):
		if target == container:
			if (target.flight_status == flight_status_dict[3]) && (target.altitude[-1] < 400):
				target = payload
