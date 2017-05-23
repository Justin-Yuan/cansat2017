import ttk, user, sys, time, datetime, thread
from Aerial import *

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
