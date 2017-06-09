import ttk, user, sys, time, datetime, thread
from Aerial import *

var_dict = {1:'data_altitude',2:'data_pressure',3:'data_pitot',4:'data_temp_outsi'}
flight_status_dict = {0: 'Initialized', 1:'Waiting', 2:'Ascending', 3:'Descending', 4:'Deploying',\
						5:'Gliding', 6:'Landed', 7:'Unknown'}

time_stamp = {'bg_container_start':0, 'bg_glider_start':0, 'tel_container_start':0}

def update_mission_time(text_var, root):
	current_time = str(datetime.datetime.now())[0: 19]
	text_var.mission_time.set("Mission Time: %s" % current_time)
	root.after(1000, update_mission_time, text_var, root)

def update_telemetry_time(text_var, root, cansat):
	text_var.telemetry_time.set("Telemetry Time: %d" % cansat.telemetry_time)
	cansat.bg_time += 1
	if cansat.telemetry_time > 1 and time_stamp['bg_container_start'] == 0:
		time_stamp['bg_container_start'] = cansat.bg_time
		time_stamp['tel_container_start'] = consat.telemetry_time
	if !cansat.switch and time_stamp['bg_glider_start'] == 0:
		time_stamp['bg_glider_start'] = cansat.bg_time
		cansat.telemetry_time = time_stamp['bg_glider_start'] - time_stamp['bg_container_start'] + time_stamp['tel_container_start']
		cansat.start_time = cansat.telemetry_time
		# to keep the glider telemetry time consistent with the container telemetry time
	root.after(1000, update_telemetry_time, text_var, root, cansat)

def update_flight_status(tel, text_var, root, cansat):
	if tel.ser_connected == True:
		text_var.flight_status.set("Flight Status: " + flight_status_dict[cansat.flight_status])
	elif tel.ser_connected == False:
		text_var.flight_status.set("Flight Status: Not Connected")
	else:
		text_var.flight_status.set("Flight Status: Unknown")

	# print tel.ser_connected

	root.after(500, update_flight_status, tel, text_var, root, cansat)

def conclude(chart):
    chart.frame.focus_set()

# in case of processor reset packet_cnt needs to be cts
# can just use a script to go through and fix any discontinuities
def check_packet_cnt():
	pass
