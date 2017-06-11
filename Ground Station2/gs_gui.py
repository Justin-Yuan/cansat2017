'''
Ground Station Framework (Rover and CanSat Projects)
Robotics for Space Exploration, University of Toronto (Canada)
University of Toronto Institute for Aerospace Studies (UTIAS)
Made by: Rahul Goel - rahul.g.eng@gmail.com

Install the necessary modules in the following order (if running into problems, uninstall and reinstall in this order for correct build):

sudo apt-get install tk tk-dev
pip install matplotlib

'''
import Tkinter
from serial import *
import ttk, user, sys, time, datetime, thread
from subprocess import check_output
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure



Team_Num = 6734
baud_rate = 9600
file_name = "CANSAT_2016.csv"

global ser, ser_connected
ser_connected = False

# Vars
force_status_var = 0
packet_cnt = 0
last_com_time = 'N/A'

## Telemetry variables
data_altitude = [0.0]
data_pressure = [0.0] 
data_pitot = [0.0]
data_temp_outside = [0.0]
data_voltage = [0.0]
data_gps_lat = [0.0]
data_gps_long = [0.0]
data_gps_alt = [0.0]
data_gps_num = 0
data_gps_speed = [0.0]
data_com_cnt = 0
data_state = 0
data_cam_angle = 0
var_dict = {1:'data_altitude',2:'data_pressure',3:'data_pitot',4:'data_temp_outside',5:'data_voltage', 6:'data_gps_lat',7:'data_gps_long',8:'data_gps_alt',9:'data_gps_num',10:'data_gps_speed',11:'data_com_cnt',12:'data_state',13:'data_cam_angle'}


def key(event):
	return
#    root.status.set(repr(event.char)) 

class menu_bar(Tkinter.Menu):
	def __init__(self, parent):
        	Tkinter.Menu.__init__(self, parent)
		self.parent = parent
		self.initialize()
	
	def initialize(self):
		filemenu = Tkinter.Menu(self, tearoff=0)
        	filemenu.add_command(label = "Save Data (.csv)", command=self.callback)
        	filemenu.add_separator()
        	filemenu.add_command(label = "Start", command = self.callback)
        	filemenu.add_command(label = "Pause", command = self.callback)
        	filemenu.add_command(label = "Stop", command = self.callback)
        	filemenu.add_separator()                
        	filemenu.add_command(label = "Exit", underline = 1, command = self.quit)
        	self.add_cascade(label="File",underline = 0, menu = filemenu)

		
		portmenu = Tkinter.Menu(self, tearoff=0)
        	found_port = False
        	for port in check_output(["ls", "/dev"]).split("\n"):
		    	if port.find("USB") != -1:
		        	found_port = True
				port_str = str(port)
				print port_str
		        	portmenu.add_command(label = port, command = lambda port_str=port_str: self.open_ser(port_str))

		portmenu.add_command(label = "Disconnect", command = self.callback)

        	if not found_port:
            		portmenu.add_command(label = "No COM Device Found")

        	self.add_cascade(label = "Establish Connection", underline = 0, menu = portmenu)

        	helpmenu = Tkinter.Menu(self, tearoff=0)
        	helpmenu.add_command(label = "About", command = self.callback)
		self.add_cascade(label = "Help", menu = helpmenu)
		

	def quit(self):
        	sys.exit(0)

	def callback(self, text = "foo"):
        	print "called the callback!"
        	print text

	def open_ser(self, port_name):
		global ser, ser_connected
		print port_name
		address = "/dev/" + port_name
		print address
        	try:
            		ser = Serial(address , baud_rate, timeout = 0, writeTimeout = 0)
            		status.set("Connected to %s" % port_name)
            		ser_connected = True
		    	print "Connected to " + port_name
			flight_status.set("Flight Status: Ready")

        	except Exception as e:
			print "Error: Connection could not be established"
            		root.status.set("Error: Connection could not be established. %s" % e)
		
class StatusBar(Tkinter.Frame):
    def __init__(self, master):
        Tkinter.Frame.__init__(self, master)
        self.label = Tkinter.Label(self, relief='sunken', anchor='w')
        self.label.pack(fill='x')
        self.set("CANSAT-2016 with RSX")

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

class main_gui(Tkinter.Tk):
	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.initialize()

	def initialize (self):
		self.geometry("1200x650+100+50")

		#MenuBar
		self.config(menu=menu_bar(self))


#### Plotting Functions
def plot_altitude():

    global fig_altitude, dataPlot_altitude, a_altitude

    fig_altitude = Figure(figsize=(4, 4), dpi = (frame.winfo_width() - 50) / 16)
    dataPlot_altitude = FigureCanvasTkAgg(fig_altitude, master = chart1_frame)
    a_altitude = fig_altitude.add_subplot(111)

    dataPlot_altitude.show()
    dataPlot_altitude.get_tk_widget().pack()

    def plot_cts():
        global a_altitude
        x_axis1 = range(0, len(data_altitude))
        x_axis2 = range(0, len(data_gps_alt))

        a_altitude.clear()
        a_altitude.plot(x_axis1, data_altitude, "r", label = "BMP180")
	a_altitude.plot(x_axis2, data_gps_alt, "b", label = "GPS")

        a_altitude.set_title("Altitude (m)")
	legend = a_altitude.legend(loc='upper left', shadow=True)       

        dataPlot_altitude.show()
        dataPlot_altitude.get_tk_widget().pack()

        root.after(1000, plot_cts)

    plot_cts()

def plot_temperature():

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

def plot_voltage():

    global fig_voltage, dataPlot_voltage, a_voltage

    fig_voltage = Figure(figsize=(4, 4), dpi = (frame.winfo_width() - 50) / 16)
    dataPlot_voltage = FigureCanvasTkAgg(fig_voltage, master = chart4_frame)

    a_voltage = fig_voltage.add_subplot(111)
    dataPlot_voltage.show()
    dataPlot_voltage.get_tk_widget().pack()    

    def plot_cts():
        global a_voltage
        a_voltage.clear()

        voltage = data_voltage[len(data_voltage) - 1]
        if voltage > 7.3:
            a_voltage.bar(0, voltage, 1, color = 'g')
        elif voltage > 5:
            a_voltage.bar(0, voltage, 1, color = 'y')
        else:
            a_voltage.bar(0, voltage, 1, color = 'r')

        a_voltage.set_title("Voltage (V)")
        a_voltage.set_ylim([0, 10])
        a_voltage.get_xaxis().set_visible(False)            

        dataPlot_voltage.show()
        dataPlot_voltage.get_tk_widget().pack() 

        root.after(1000, plot_cts)

    plot_cts()    

def plot_pitot():

    global fig_pitot, dataPlot_pitot, a_pitot

    fig_pitot = Figure(figsize=(4, 4), dpi = (frame.winfo_width() - 50) / 16)
    dataPlot_pitot = FigureCanvasTkAgg(fig_pitot, master = chart3_frame)

    a_pitot = fig_pitot.add_subplot(111)
    dataPlot_pitot.show()
    dataPlot_pitot.get_tk_widget().pack() 
  
    def plot_cts():
        global a_pitot
	x_axis1 = range(0, len(data_pitot))
	x_axis2 = range(0, len(data_gps_speed))

        a_pitot.clear()
        a_pitot.plot(x_axis1, data_pitot, "r", label = "Pitot")
        a_pitot.plot(x_axis2, data_gps_speed, "b", label = "GPS")

        a_pitot.set_title("Speed (m/s)")
        a_pitot.set_ylim([-10, 100])
	legend = a_pitot.legend(loc='upper left', shadow=True)             

        dataPlot_pitot.show()
        dataPlot_pitot.get_tk_widget().pack() 

        root.after(1000, plot_cts)

    plot_cts() 
                                                                                                                                                                 
def ser_test_write():
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
	str_time = str(datetime.datetime.now())[0:19]
	mission_time.set("Mission Time: %s" % str_time)
	root.after(1000,update_mission_time)

def update_flight_status():
	if ser_connected == 1:
		if data_state == 1:
			flight_status.set("Flight Status: Waiting")
		elif data_state == 2:
			flight_status.set("Flight Status: Ascending")
		elif data_state == 3:
			flight_status.set("Flight Status: Descending")
		elif data_state == 4:
			flight_status.set("Flight Status: Deploying (410 m reached)")
		elif data_state == 5:
			flight_status.set("Flight Status: Gliding")
		elif data_state == 6:
			flight_status.set("Flight Status: Landed")
		else: 
			flight_status.set("Flight Status: Unknown")
	else: 
		if ser_connected == 0:
			flight_status.set("Flight Status: Not Connected")
		else:
			flight_status.set("Flight Status: Unknown")
	root.after(200, update_flight_status)

def update_left_ribbon():
	pack_cnt.set("Packet Cnt: %d" % packet_cnt)
	pressure_var.set("Atm Pressure %.1f kPa" % data_pressure[-1])
	gps_lat.set("GPS Latitude: %.4f" % data_gps_lat[-1])
	gps_long.set("GPS Longitude: %.4f" % data_gps_long[-1])
	gps_num.set("GPS # Sat: %d" % data_gps_num)	
	com_cnt.set("Command Sent: %d" % data_com_cnt)
	cam_angle_text.set("Current Cam Angle: %d Degrees" % data_cam_angle)
	last_com.set("Last Cmd: %s" % last_com_time)
	root.after(1000, update_left_ribbon)	

def snap_button_callback():
	try:
		if ser_connected == 1:
			ser.write("s \n")
			print 'snap command sent'
	except Exception as e:
		print "Error: Could not write to serial"
    		root.status.set("Error: Could not write to serial. %s" % e)

def move_button_callback():
	try:
		if ser_connected == 1:
			cam_delta = float(cam_angle_entry.get())

			if cam_delta > 0 and cam_delta < 180:
				ser.write('m %d\n' % cam_delta)
				print 'move command sent with %d degrees' % cam_delta
			else:
				print 'Use valid cam angle'
	except Exception as e:
		print "Error: Could not write to serial"
    		root.status.set("Error: Could not write to serial. %s" % e)
		

def force_status_callback(status):
	global force_status_var
	if status == 1:
		force_status.set("Deploy Selected")
		force_status_var = 1
	elif status == 2:
		force_status.set("Land Selected")
		force_status_var = 2
	else:
		force_status.set("None Selected")
		force_status_var = 0


def execute_button_callback():
	try:
		if ser_connected == 1:

			if force_status_var == 1 or force_status_var == 2:
				ser.write('f %d\n' % force_status_var)
				print 'force command sent with %d' % force_status_var
			else:
				print 'Nothing was executed'

	except Exception as e:
		print "Error: Could not write to serial"
    		root.status.set("Error: Could not write to serial. %s" % e)

def conclude():
    frame.focus_set()

if __name__ == "__main__":
	f = open(file_name, "a")
	f.write("TEAM ID,Pack Cnt,Altitude,Pressure,Speed,Temp,Voltage,GPS Lat,GPS Long,GPS Alt,GPS Sat#,GPS Speed,Com Time,Com Cnt,Flight State,Cam Angle\n")
	f.close()

	root = main_gui(None)
	root.title('CANSAT - 2016   Team: ' + str(Team_Num))

	# Text Var
	mission_time = Tkinter.StringVar()
	force_status = Tkinter.StringVar()
	force_status.set("None Selected")
	flight_status = Tkinter.StringVar()
	flight_status.set("Flight Status: Not Connected")
	pack_cnt = Tkinter.StringVar()
	pack_cnt.set("Packet Cnt: %d" % packet_cnt)
	pressure_var = Tkinter.StringVar()
	pressure_var.set("Atm Pressure %d kPa" % data_pressure[-1])
	gps_lat = Tkinter.StringVar()
	gps_lat.set("GPS Latitude: %d" % float(data_gps_lat[-1]))
	gps_long = Tkinter.StringVar()
	gps_long.set("GPS Longitude: %d" % float(data_gps_long[-1]))
	gps_num = Tkinter.StringVar()
	gps_num.set("GPS # Sat: %d" % data_gps_num)	
	com_cnt = Tkinter.StringVar()
	com_cnt.set("Command Sent: %d" % data_com_cnt)	
	last_com = Tkinter.StringVar()
	last_com.set("Last Cmd: %s" % last_com_time)
	cam_angle_text = Tkinter.StringVar()
	cam_angle_text.set("Current Cam Angle: %d Degrees" % data_cam_angle)
	cam_angle_entry = Tkinter.StringVar()
	
 

	# Top info bar (team, time, flight status)
	top_info_frame = Tkinter.Frame(root, bg='black')
	top_info_frame.pack(side = "top", expand = 1, fill = 'x')
	label_top1 = Tkinter.Label(top_info_frame, text = "TEAM #6734",fg='white',bg='black')
	label_top1.pack(side='left', expand = 1, fill = 'x')

	mission_time.set("Mission Time: %s" % str(datetime.datetime.now())[0:19])
	label_top2 = Tkinter.Label(top_info_frame, textvariable = mission_time, fg='white',bg='black')
	label_top2.pack(side='left', expand = 1, fill = 'x')
	label_top3 = Tkinter.Label(top_info_frame, textvariable = flight_status,fg='white',bg='black') 
	label_top3.pack(side='left', expand = 1, fill = 'x')

	# left ribbon
	left_ribbon = Tkinter.Frame(root)
	left_ribbon.pack(side = "left", expand = 1, padx = 20, fill = 'y')

	# other info bar (team, time, flight status)
	info_frame = Tkinter.Frame(left_ribbon)
	info_frame.pack(side = "top",expand = 1,  fill = 'both')
	label_info0 = Tkinter.Label(info_frame, textvariable = pack_cnt )
	label_info0.grid(column = 0, row = 0,sticky = 'w')
	label_info4 = Tkinter.Label(info_frame, textvariable = pressure_var )
	label_info4.grid(column = 0, row = 1,sticky = 'w')
	label_info1 = Tkinter.Label(info_frame, textvariable = gps_lat)
	label_info1.grid(column = 0, row = 2,sticky = 'w')
	label_info2 = Tkinter.Label(info_frame, textvariable = gps_long)
	label_info2.grid(column = 0, row = 3,sticky = 'w')
	label_info3 = Tkinter.Label(info_frame, textvariable = gps_num)
	label_info3.grid(column = 0, row = 4,sticky = 'w')

	# Camera Operations
	cam_button_frame1 = Tkinter.Frame(left_ribbon)
	cam_button_frame1.pack(side = "top", expand = 1, fill = 'both')
	cam_angle = Tkinter.Entry(cam_button_frame1, textvariable = cam_angle_entry)
	cam_angle.grid(column = 0,row = 0)
	cam_angle.bind("<Return>")
	cam_move = Tkinter.Button(cam_button_frame1,text=u"Move",command = move_button_callback)
	cam_move.grid(column = 1, row = 0)
	cam_angle = Tkinter.Label(cam_button_frame1, textvariable = cam_angle_text)
	cam_angle.grid(column = 0, row = 1,columnspan = 2)

	cam_button_frame2 = Tkinter.Frame(left_ribbon)
	cam_button_frame2.pack(side = "top", expand = 1, fill = 'both')
	button_pic = Tkinter.Button(cam_button_frame2,pady = 10,text=u"Snap Image",command = snap_button_callback)
	button_pic.pack(side = 'top', fill = 'both')
	cam_cmd = Tkinter.Label(cam_button_frame2, textvariable = com_cnt)
	cam_cmd.pack(side = 'top', fill = 'x')
	last_cam_cmd = Tkinter.Label(cam_button_frame2, textvariable = last_com)
	last_cam_cmd.pack(side = 'top', fill = 'x')

	# Force Button	 
	status_button_frame = Tkinter.Frame(left_ribbon, bg = 'red')
	status_button_frame.pack(side = "top", expand = 1, fill = 'both')
	label_force = Tkinter.Label(status_button_frame, text = "FORCE ACTIONS",bg = 'red')
	label_force.pack(side = 'top', fill = 'both')
	button_none = Tkinter.Button(status_button_frame,text=u"None",command = lambda x=0: force_status_callback(x))
	button_none.pack(side = 'top')
	button_deploy = Tkinter.Button(status_button_frame,text=u"Deploy",command = lambda x=1: force_status_callback(x))
	button_deploy.pack(side = 'top')
	button_land = Tkinter.Button(status_button_frame,text=u"Land",command = lambda x=2: force_status_callback(x))
	button_land.pack(side = 'top')

	label_force_status = Tkinter.Label(status_button_frame, textvariable = force_status ,pady=12, bg = 'red')
	label_force_status.pack(side = 'top',fill = 'x')

	button_act = Tkinter.Button(status_button_frame, text = "Execute",command = execute_button_callback)
	button_act.pack(side = 'top')
		
	# Main chart area
	frame = Tkinter.Frame(root)
	frame.pack(side='top', expand = 1, fill='x')
	frame.bind("<Key>", key)
	frame.focus_set()

	chart1_frame = Tkinter.Frame(frame)
	chart1_frame.pack(side = "left", expand = 1, fill = 'both')
	chart2_frame = Tkinter.Frame(frame)
	chart2_frame.pack(side = "left", expand = 1, fill = 'both')
	chart3_frame = Tkinter.Frame(frame)
	chart3_frame.pack(side = "left", expand = 1, fill = 'both')
	chart4_frame = Tkinter.Frame(frame)
	chart4_frame.pack(side = "left", expand = 1, fill = 'both')

	# Scroll Telemetry
	stream_frame = Tkinter.Frame(root, bg = "white")
	stream_frame.pack(side = "top", pady = 0, fill = 'both', expand = True)

	scrollbar = Tkinter.Scrollbar(stream_frame)
	scrollbar.pack(side = 'right', fill = 'y')

	listbox = Tkinter.Listbox(stream_frame, width = 600,height = 20, yscrollcommand=scrollbar.set)
	listbox.pack(side ='left', fill = 'both')
	scrollbar.config(command=listbox.yview)
	

	# Bottom status bar
	status = StatusBar(root)
	status.pack(side='bottom', fill='x')


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
	



