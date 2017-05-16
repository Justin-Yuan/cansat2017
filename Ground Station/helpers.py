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
