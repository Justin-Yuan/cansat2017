from serial import *
from subprocess import check_output
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from tkFileDialog import asksaveasfile
import csv
import datetime

from helpers import *
try:
    # for Python2
    import Tkinter as Tk
except:
    # for Python3
    import tkinter as Tk

baud_rate = 9600

class MainGUI(Tk.Tk):
    def __init__(self,parent, cansat, tel):
        Tk.Tk.__init__(self,parent)
        self.parent = parent
        self.geometry("1200x800+100+50")
        self.config(menu=MenuBar(self, cansat, tel))


class MenuBar(Tk.Menu):
    """
    """
    def __init__(self, parent, cansat, tel):
        Tk.Menu.__init__(self, parent)
        self.parent = parent
        self.tel = tel
        # self.text_var = text_var
        self.initialize()
        self.cansat = cansat

    def initialize(self):
        # File menu
        self.file_menu = Tk.Menu(self, tearoff=0)
        # self.file_menu.add_command(label="Save", command=self.save_data)
        # self.file_menu.add_separator()
        self.file_menu.add_command(label="Start", command=self.start_operation)
        self.file_menu.add_command(label="Pause", command=self.pause_operation)
        self.file_menu.add_command(label="Stop", command=self.stop_operation)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", underline=1, command=self.quit)
        self.add_cascade(label="File", underline=0, menu=self.file_menu)

        # Connection menu
        port_menu = Tk.Menu(self, tearoff=0)
        found_port = False
        for port in check_output(["ls", "/dev"]).split("\n"):
            if port.find("USB") != -1:
                found_port = True
                usb_port = str(port)
                print(usb_port)
                port_menu.add_command(label=port, command=lambda usb_port=usb_port: self.open_ser(usb_port, self.tel))

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

    def open_ser(self, usb_port, tel):
        print "trying to connect..."
        address = "/dev/" + usb_port
        try:
            tel.ser = Serial(address, baud_rate, timeout=0, writeTimeout=0)
            # text_var.flight_status.set("Connected to %s" % usb_port)
            print "Connected to %s" % usb_port
            tel.ser_connected = True
            print("Connected to " + usb_port)
            # flight_status.set("Flight Status: Ready")
        except Exception as e:
            print("Error:connection cannot be established")
            print(e)
            # root.status.set("Error: connection cannot be established. %s" % e)

    def disconnect(self, usb_port, tel):
        tel.ser.close()
        tel.ser_connected = False
        print("Ended connection")
        flight_status.set("Flight Status: Standby")


class StatusBar(Tk.Frame):
    """
    """
    def __init__(self, parent):
        Tk.Frame.__init__(self, parent)
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

    def __init__(self, parent, cansat):
        self.cansat = cansat
        self.frame = Tk.Frame(parent)
        self.frame2 = Tk.Frame(parent)
        self.chart1_frame = Tk.Frame(self.frame)
        self.chart2_frame = Tk.Frame(self.frame)
        self.chart3_frame = Tk.Frame(self.frame)
        self.chart4_frame = Tk.Frame(self.frame)
        self.chart5_frame = Tk.Frame(self.frame2)
        self.chart6_frame = Tk.Frame(self.frame2)
        self.chart7_frame = Tk.Frame(self.frame2)

        self.pack_frame()

    def pack_frame(self):
        self.frame.pack(side='top', expand = 1, fill='x')
        self.frame.bind("<Key>", self.key)
        self.frame.focus_set()

        self.chart1_frame.pack(side = "left", expand = 1, fill = 'both')
        self.chart2_frame.pack(side = "left", expand = 1, fill = 'both')
        self.chart3_frame.pack(side = "left", expand = 1, fill = 'both')
        self.chart4_frame.pack(side = "left", expand = 1, fill = 'both')

        self.frame2.pack(expand = 1, fill='x')
        self.frame.bind("<Key>", self.key)

        self.chart5_frame.pack(side = "left", expand = 1, fill = 'both')
        self.chart6_frame.pack(side = "left", expand = 1, fill = 'both')
        self.chart7_frame.pack(side = "left", expand = 1, fill = 'both')


    def key(self, event):
        return
#    root.status.set(repr(event.char))
    def plot_altitude(self):
        global fig_altitude, dataPlot_altitude, a_altitude

        fig_altitude = Figure(figsize=(4, 4), dpi = (self.frame.winfo_width() - 50) / 16)
        dataPlot_altitude = FigureCanvasTkAgg(fig_altitude, master = self.chart1_frame)
        a_altitude = fig_altitude.add_subplot(111)

        dataPlot_altitude.show()
        dataPlot_altitude.get_tk_widget().pack()

        def plot_cts():
            global a_altitude
            x_axis1 = range(0, len(self.cansat.altitude))
            # x_axis2 = range(0, len(self.cansat.gps_alt))

            # print self.cansat.identifier

            a_altitude.clear()
            a_altitude.plot(x_axis1, self.cansat.altitude, "r", label = "BMP180")
            # a_altitude.plot(x_axis2, self.cansat.gps_alt, "b", label = "GPS")


            a_altitude.set_title("Altitude (m)")
            legend = a_altitude.legend(loc='upper left', shadow=True)

            dataPlot_altitude.show()
            dataPlot_altitude.get_tk_widget().pack()

            self.chart1_frame.after(1000, plot_cts)

        plot_cts()

    def plot_pressure(self):
        global fig_pressure, dataPlot_pressure, a_pressure

        fig_pressure = Figure(figsize=(4, 4), dpi = (self.frame.winfo_width() - 50) / 16)
        dataPlot_pressure = FigureCanvasTkAgg(fig_pressure, master = self.chart3_frame)
        a_pressure = fig_pressure.add_subplot(111)

        dataPlot_pressure.show()
        dataPlot_pressure.get_tk_widget().pack()

        def plot_cts():
            global a_pressure
            x_axis1 = range(0, len(self.cansat.pressure))
            # x_axis2 = range(0, len(self.cansat.gps_alt))

            # print self.cansat.identifier

            a_pressure.clear()
            a_pressure.plot(x_axis1, self.cansat.pressure, "r", label = "BMP180")
            # a_altitude.plot(x_axis2, self.cansat.gps_alt, "b", label = "GPS")

            a_pressure.set_title("Pressure (kPa)")

            dataPlot_pressure.show()
            dataPlot_pressure.get_tk_widget().pack()

            self.chart3_frame.after(1000, plot_cts)

        plot_cts()

    def plot_temperature(self):
        # global root
        # root = tk.Tk()
        global fig_temp, dataPlot_temp, a_temp

        fig_temp = Figure(figsize=(4, 4), dpi = (self.frame.winfo_width() - 50) / 16)
        dataPlot_temp = FigureCanvasTkAgg(fig_temp, master = self.chart2_frame)
        a_temp = fig_temp.add_subplot(111)

        dataPlot_temp.show()
        dataPlot_temp.get_tk_widget().pack()

        def plot_cts():
            global a_temp
            x_axis = range(0, len(self.cansat.temp_outside))

            a_temp.clear()
            a_temp.plot(x_axis, self.cansat.temp_outside, "r", label = "Outside")

            a_temp.set_title("Temperature (C)")
            a_temp.set_ylim([0, 60])

            dataPlot_temp.show()
            dataPlot_temp.get_tk_widget().pack()

            self.chart2_frame.after(1000, plot_cts)

        plot_cts()

    def plot_voltage(self):
        global fig_voltage, dataPlot_voltage, a_voltage

        fig_voltage = Figure(figsize=(4, 4), dpi = (self.frame.winfo_width() - 50) / 16)
        dataPlot_voltage = FigureCanvasTkAgg(fig_voltage, master =self.chart4_frame)

        a_voltage = fig_voltage.add_subplot(111)
        dataPlot_voltage.show()
        dataPlot_voltage.get_tk_widget().pack()

        def plot_cts():
            global a_voltage
            a_voltage.clear()
            voltage = self.cansat.voltage[len(self.cansat.voltage) - 1]
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

            self.chart4_frame.after(1000, plot_cts)

        plot_cts()

    def plot_pitot(self):
        global fig_pitot, dataPlot_pitot, a_pitot

        fig_pitot = Figure(figsize=(4, 4), dpi = (self.frame.winfo_width() - 50) / 16)
        dataPlot_pitot = FigureCanvasTkAgg(fig_pitot, master = self.chart5_frame)

        a_pitot = fig_pitot.add_subplot(111)
        dataPlot_pitot.show()
        dataPlot_pitot.get_tk_widget().pack()

        def plot_cts():
            global a_pitot
            target = self.cansat
            x_axis1 = range(0, len(target.pitot))
            # x_axis2 = range(0, len(target.gps_speed))

            a_pitot.clear()
            a_pitot.plot(x_axis1, target.pitot, "r", label = "Pitot")
            # a_pitot.plot(x_axis2, target.gps_speed, "b", label = "GPS")

            a_pitot.set_title("Speed (m/s)")
            a_pitot.set_ylim([-10, 100])
            legend = a_pitot.legend(loc='upper left', shadow=True)

            dataPlot_pitot.show()
            dataPlot_pitot.get_tk_widget().pack()

            self.chart5_frame.after(1000, plot_cts)

        plot_cts()

    def plot_heading(self):
        global fig_heading, dataPlot_heading, a_heading

        fig_heading = Figure(figsize=(4, 4), dpi = (self.frame.winfo_width() - 50) / 16)
        dataPlot_heading = FigureCanvasTkAgg(fig_heading, master = self.chart6_frame)

        a_heading = fig_heading.add_subplot(111)
        dataPlot_heading.show()
        dataPlot_heading.get_tk_widget().pack()

        def plot_cts():
            global a_heading
            target = self.cansat
            x_axis1 = range(0, len(target.heading))
            # x_axis2 = range(0, len(target.gps_speed))

            a_heading.clear()
            a_heading.plot(x_axis1, target.heading, "r", label = "Heading")
            # a_pitot.plot(x_axis2, target.gps_speed, "b", label = "GPS")

            a_heading.set_title("Heading (degree)")
            a_heading.set_ylim([-10, 100])
            legend = a_heading.legend(loc='upper left', shadow=True)

            dataPlot_heading.show()
            dataPlot_heading.get_tk_widget().pack()

            self.chart6_frame.after(1000, plot_cts)

        plot_cts()

    def plot_position(self):
        # global root
        # root = tk.Tk()
        global fig_position, dataPlot_position, a_position

        fig_position = Figure(figsize=(4, 4), dpi = (self.frame.winfo_width() - 50) / 16)
        dataPlot_position = FigureCanvasTkAgg(fig_position, master = self.chart7_frame)
        a_position = fig_position.add_subplot(111)

        dataPlot_position.show()
        dataPlot_position.get_tk_widget().pack()

        def plot_cts():
            global a_position
            # x_axis = range(0, len(self.cansat.pos_x))

            a_position.clear()
            a_position.plot(self.cansat.pos_x, self.cansat.pos_y, "r", label = "2D_position")

            a_position.set_title("2D Position")
            # a_position.set_ylim([0, 60])

            dataPlot_position.show()
            dataPlot_position.get_tk_widget().pack()

            self.chart7_frame.after(1000, plot_cts)

        plot_cts()


class Panel(Tk.Frame):
    """ Panel for showing current data
    """
    def __init__(self, parent, cansat):
        Tk.Frame.__init__(self, parent)
        self.pack(side = "left", expand = 1, padx = 20, fill = 'y')
        self.cansat = cansat

# TODO need to add a target here: whether it's container or payload
    def update_panel(self, root, target, text_var):
        text_var.pack_cnt.set("Packet Cnt: %d" % target.packet_cnt)
        text_var.pressure_var.set("Atm Pressure %.1f kPa" % target.pressure[-1])
        # text_var.gps_lat.set("GPS Latitude: %.4f" % target.gps_lat[-1])
        # text_var.gps_long.set("GPS Longitude: %.4f" % target.gps_long[-1])
        # text_var.gps_num.set("GPS # Sat: %d" % target.gps_num)

        root.after(1000, self.update_panel, root, target, text_var)


class TextVar(object):
    """ TextVar object to group text labels
    """
    def __init__(self, root, cansat):
        self.mission_time = Tk.StringVar()
        self.telemetry_time = Tk.StringVar()

        self.force_status = Tk.StringVar()
        self.flight_status = Tk.StringVar()
        self.pack_cnt = Tk.StringVar()
        self.packet_cnt_glider = Tk.StringVar()

        self.altitude_var = Tk.StringVar()
        self.temperature_var = Tk.StringVar()
        self.pressure_var = Tk.StringVar()
        self.voltage_var = Tk.StringVar()
        self.speed_var = Tk.StringVar()
        self.heading_var = Tk.StringVar()

        self.pos_x_var = Tk.StringVar()
        self.pos_y_var = Tk.StringVar()

        # not in use
        self.gps_lat = Tk.StringVar()
        self.gps_long = Tk.StringVar()
        self.gps_num = Tk.StringVar()
        self.glider_status = Tk.StringVar()
        # not in use

        self.cansat = cansat
        self.set_text(root)


    def set_text(self, root):
        self.glider_status.set("Current: " + self.cansat.identifier)
        self.force_status.set("None Selected")
        self.flight_status.set("Flight Status: Not Connected")

        self.pack_cnt.set("Packet Cnt: %d" % self.cansat.packet_cnt)
        self.packet_cnt_glider.set("Glider Packet Cnt: %d" % self.cansat.packet_cnt_glider)
        self.altitude_var.set("Altitude: %g (m)" % self.cansat.altitude[-1])
        self.temperature_var.set("Temperature: %g (C)" % self.cansat.temp_outside[-1])
        self.pressure_var.set("Pressure: %g (kPa)" % self.cansat.pressure[-1])
        self.voltage_var.set("Voltage: %g (V)" % self.cansat.voltage[-1])
        self.speed_var.set("Speed: %g (m/s)" % self.cansat.pitot[-1])
        self.heading_var.set("Heading: %g (deg)" % self.cansat.heading[-1])

        self.pos_x_var.set("X: %g" % self.cansat.pos_x[-1])
        self.pos_y_var.set("Y: %g" % self.cansat.pos_y[-1])

        root.after(1000, self.set_text, root)

class TopInfoFrame(Tk.Frame):
    """
    """
    def __init__(self, parent, text_var, TEAM_NUM):
        self.top_info_frame = Tk.Frame(parent, bg='black')
        # TODO change TEAM_NUM
        self.label_top1 = Tk.Label(self.top_info_frame, text = "TEAM #"+str(TEAM_NUM), fg='white', bg='black')
        self.label_top2 = Tk.Label(self.top_info_frame, textvariable = text_var.mission_time, fg='white', bg='black')
        self.label_top3 = Tk.Label(self.top_info_frame, textvariable = text_var.flight_status, fg='white', bg='black')
        self.label_top4 = Tk.Label(self.top_info_frame, textvariable = text_var.glider_status, fg='white', bg='black')
        self.pack_frame()

    def pack_frame(self):
        self.top_info_frame.pack(side = "top", expand = 1, fill = 'x')
        self.label_top1.pack(side='left', expand = 1, fill = 'x')
        self.label_top2.pack(side='left', expand = 1, fill = 'x')
        self.label_top3.pack(side='left', expand = 1, fill = 'x')
        self.label_top4.pack(side='left', expand = 1, fill = 'x')


class LeftInfoFrame(Tk.Frame):
    """
    """
    def __init__(self, parent, text_var):
        self.info_frame = Tk.Frame(parent)
        self.label_info0 = Tk.Label(self.info_frame, textvariable = text_var.telemetry_time)
        self.label_info1 = Tk.Label(self.info_frame, textvariable = text_var.pack_cnt)
        self.label_info2 = Tk.Label(self.info_frame, textvariable= text_var.packet_cnt_glider)
        self.label_info3 = Tk.Label(self.info_frame, textvariable = text_var.altitude_var)
        self.label_info4 = Tk.Label(self.info_frame, textvariable = text_var.temperature_var)
        self.label_info5 = Tk.Label(self.info_frame, textvariable = text_var.pressure_var)
        self.label_info6 = Tk.Label(self.info_frame, textvariable= text_var.voltage_var)
        self.label_info7 = Tk.Label(self.info_frame, textvariable = text_var.speed_var)
        self.label_info8 = Tk.Label(self.info_frame, textvariable = text_var.heading_var)

        self.label_info9 = Tk.Label(self.info_frame, textvariable = text_var.pos_x_var)
        self.label_info10 = Tk.Label(self.info_frame, textvariable = text_var.pos_y_var)

        # self.label_info1 = Tk.Label(self.info_frame, textvariable = text_var.gps_lat)
        # self.label_info2 = Tk.Label(self.info_frame, textvariable = text_var.gps_long)
        # self.label_info3 = Tk.Label(self.info_frame, textvariable = text_var.gps_num)

        self.pack_frame()

    def pack_frame(self):
        self.info_frame.pack(side = "top",expand = 1,  fill = 'both')
        self.label_info0.grid(column = 0, row = 0, sticky = 'w')
        self.label_info1.grid(column = 0, row = 1,sticky = 'w')
        self.label_info2.grid(column = 0, row = 2,sticky = 'w')
        self.label_info3.grid(column = 0, row = 3, sticky = 'w')
        self.label_info4.grid(column = 0, row = 4, sticky = 'w')
        self.label_info5.grid(column = 0, row = 5,sticky = 'w')
        self.label_info6.grid(column = 0, row = 6,sticky = 'w')
        self.label_info7.grid(column = 0, row = 7, sticky = 'w')
        self.label_info8.grid(column = 0, row = 8, sticky = 'w')

        self.label_info9.grid(column = 0, row = 9, sticky = 'w')
        self.label_info10.grid(column = 0, row = 10, sticky = 'w')

        # self.label_info1.grid(column = 0, row = 2,sticky = 'w')
        # self.label_info2.grid(column = 0, row = 3,sticky = 'w')
        # self.label_info3.grid(column = 0, row = 4,sticky = 'w')


class ForceFrame(Tk.Frame):
    """
    """
    def __init__(self, parent, text_var, force_status_var, telemetry):
        self.force_status_var = force_status_var
        self.tel = telemetry

        self.status_button_frame = Tk.Frame(parent, bg = 'red')
        self.force_status = text_var.force_status

        self.label_force = Tk.Label(self.status_button_frame, text = "FORCE ACTIONS",bg = 'red')
        self.button_none = Tk.Button(self.status_button_frame,text=u"None",command = lambda x=0: self.force_status_callback(x))
        self.button_deploy = Tk.Button(self.status_button_frame,text=u"Deploy",command = lambda x=1: self.force_status_callback(x))
        self.button_land = Tk.Button(self.status_button_frame,text=u"Land",command = lambda x=2: self.force_status_callback(x))
        self.label_force_status = Tk.Label(self.status_button_frame, textvariable = self.force_status ,pady=12, bg = 'red')
        self.button_act = Tk.Button(self.status_button_frame, text = "Execute",command = self.execute_button_callback())

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
    def force_status_callback(self, status):
        if status == 1:
            self.force_status.set("Deploy Selected")
            self.force_status_var = 1
        elif status == 2:
            self.force_status.set("Land Selected")
            self.force_status_var = 2
        else:
            self.force_status.set("None Selected")
            self.force_status_var = 0

# TODO ser_connected variable and ser variable
    def execute_button_callback(self):
        try:
            if self.tel.ser_connected == 1:
                if force_status_var == 1 or force_status_var == 2:
                    self.tel.ser.write('f %d\n' % force_status_var)
                    print 'force command sent with %d' % force_status_var
                else:
                    print 'Nothing was executed'
        except Exception as e:
            print "Error: Could not write to serial"
            # ????
            self.force_status.set("Error: Could not write to serial. %s" % e)


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
