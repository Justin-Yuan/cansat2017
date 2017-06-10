from random import randint, uniform
import math
import datetime
import helpers
import csv
class Cansat(object):
    """ Cansat class to encapsulate shared variables and functions
    """
    def __init__(self):
        self.packet_cnt = 0
        self.packet_cnt_glider = 0
        self.altitude = [0.0]
        self.mission_time = str(datetime.datetime.now())[14:19]
        self.telemetry_time = 0
        self.bg_time = 0    # background time
        self.pressure = [0.0] # glider only
        self.pitot = [0.0]
        self.temp_outside = [0.0]
        self.voltage = [0.0]  # solar power voltage for glider
        self.heading = [0.0]  # glider only
        self.flight_status = 0
        self.identifier = "CONTAINER"
        self.switch = True

        # for 2D plot
        self.start_time = 0
        self.x_change = 0
        self.y_change = 0
        self.new_x = 0
        self.new_y = 0
        self.pos_x = [0.0]
        self.pos_y = [0.0]

        # for packet count fallback
        self.packet_cnt_store = 0
        self.packet_cnt_glider_store = 0

    def update_identifier(self, root):
        if self.flight_status == 3  \
        and self.altitude[-1] < 400\
        and self.identifier == "CONTAINER":
            if self.identifier == "CONTAINER":
                self.identifier = "GLIDER"
        root.after(1000, self.update_identifier, root)

# class Container(Cansat):
#     """
#     """
#     def __init__(self):
#         Cansat.__init__(self)
#         self.identifier = "CONTAINER"
#
#
# class Payload(Cansat):
#     """
#     """
#     def __init__(self):
#         Cansat.__init__(self)
#         self.identifier = "GLIDER"

class Telemetry(object):
    """
    """
    def __init__(self, cansat, file_name):
        self.ser = None
        self.ser_connected = False
        self.cansat = cansat
        # for testing wihtout serial only
        self.csv_test = False
        # self.switch = True
        self.file_name = file_name

    def find_position_change(self, time, speed, degree):
        speed_2d = math.sqrt(abs(math.pow(speed, 2.0) - math.pow(9.81*(time-self.cansat.start_time), 2.0)))
        return speed_2d*math.cos(degree/180*math.pi), speed_2d*math.sin(degree/180*math.pi)

    def serial_update_write(self, root, telemetry_box):
        print "connection: " + str(self.ser_connected)

        # for testing plots without serial connection only, delete this later
        if self.csv_test:
            altitude = randint(1, 400)
            pressure = randint(101, 120) #1
            pitot = randint(30,40) #2
            temp_outside = randint(22, 32) #3
            voltage = uniform(0, 8) #4
            gps_lat = randint(0, 100) #5
            gps_long = randint(0, 100) #6
            gps_alt = randint(0, 1000) #7
            gps_num = randint(0, 10) #8
            gps_speed = randint(30,40) #9
            com_cnt = randint(0,3) #10
            state = randint(1,7) #11
            tel_time = randint(1, 20)
            angle = randint(-180,180) #12
            x = randint(0, 10)
            y = randint(0, 10)
            # heading?
            heading = randint(0,10) #idk
            self.cansat.packet_cnt += 1
            self.cansat.mission_time = str(datetime.datetime.now())[14:19]
            self.cansat.altitude.append(altitude)
            self.cansat.pressure.append(pressure)
            self.cansat.temp_outside.append(temp_outside)
            self.cansat.voltage.append(voltage)
            self.cansat.pitot.append(pitot)
            self.cansat.heading.append(heading)
            self.cansat.flight_status = state
            self.cansat.pos_x.append(x)
            self.cansat.pos_y.append(y)
            self.cansat.telemetry_time = tel_time

        # TO-DO: verify the data_list fields
        elif self.ser_connected:
            """ message format
            container:
                6159, CONTAINER, time, pct count, altitude, temperature, voltage, state \n
            glider:
                6159, GLIDER, pct count, altitude, pressure, speed, temperature, voltage, heading, state \n
            """

            data = self.ser.readline()
            data_list = data.split(",")
            telemetry_box.listbox.insert(0, data)
            #listbox.insert(0, ["TEST ",data_list])
            print data_list
            if len(data_list) == 8:
                self.cansat.identifier = "CONTAINER"
                #listbox.insert(0, ["TEST ",data_list])

                for i in range(0,8):
                    if (data_list[i] == "" or data_list[i][0] == '-'):
                        data_list[i] = str(000)

                    try:
                        float(data_list[i])
                    except:
                        data_list[i] = str(000)

                # TODO: telemetry packet cnt
                if int(data_list[3]) + self.cansat.packet_cnt_store < self.cansat.packet_cnt + 1:
                    self.cansat.packet_cnt_store = self.cansat.packet_cnt
                    print "packet count mismatch"
                elif int(data_list[3]) > self.cansat.packet_cnt + 1:
                    print "missed packet"
                self.cansat.packet_cnt = int(data_list[3]) + self.cansat.packet_cnt_store
                # self.cansat.packet_cnt += 1

                self.cansat.pitot.append(0.0)
                self.cansat.altitude.append(float(data_list[4]))
                self.cansat.temp_outside.append(float(data_list[5]))
                self.cansat.voltage.append(float(data_list[6]))
                self.cansat.pressure.append(0.0)
                self.cansat.heading.append(0.0)
                self.cansat.telemetry_time = int(data_list[2])
                self.cansat.flight_status = int(data_list[7][0])
                self.cansat.pos_x.append(0.0)
                self.cansat.pos_y.append(0.0)
            elif len(data_list) == 10:
                self.cansat.identifier = "GLIDER"

                for i in range(0,10):
                    if (data_list[i] == "" or data_list[i][0] == '-'):
                        data_list[i] = str(000)

                    try:
                        float(data_list[i])
                    except:
                        data_list[i] = str(000)

                # TODO: telemetry packet cnt index
                if int(data_list[2]) + self.cansat.packet_cnt_glider_store \
                < self.cansat.packet_cnt_glider + 1:
                    self.cansat.packet_cnt_glider_store = self.cansat.packet_cnt_glider
                    print "packet count mismatch"
                elif int(data_list[2]) > self.cansat.packet_cnt_glider + 1:
                    print "missed packet"
                self.cansat.packet_cnt_glider = int(data_list[2]) + self.cansat.packet_cnt_glider_store
                # self.cansat.packet_cnt_glider += 1

                self.cansat.pitot.append(float(data_list[5]))
                self.cansat.altitude.append(float(data_list[3]))
                self.cansat.temp_outside.append(float(data_list[6]))
                self.cansat.voltage.append(float(data_list[7]))
                self.cansat.pressure.append(float(data_list[4]))
                self.cansat.heading.append(float(data_list[8]))

                if self.cansat.switch:
                    self.cansat.switch = False
                    # self.cansat.telemetry_time += 3

                    # self.start_time = self.cansat.telemetry_time
                    self.cansat.pos_x.append(0.0)
                    self.cansat.pos_y.append(0.0)
                else:
                    self.cansat.telemetry_time += 1
                    (self.cansat.x_change, self.cansat.y_change) = self.find_position_change(self.cansat.telemetry_time,
                                                                        self.cansat.pitot[-1], self.cansat.heading[-1])
                    self.cansat.new_x += self.cansat.x_change
                    self.cansat.new_y += self.cansat.y_change
                    self.cansat.pos_x.append(self.cansat.new_x)
                    self.cansat.pos_y.append(self.cansat.new_y)

                self.cansat.flight_status = int(data_list[9][0])

        root.after(1000, self.serial_update_write, root, telemetry_box)

    def write_to_csv(self, root): # writes in parallel with the serial update
        with open(self.file_name, 'aw+') as csvfile:
            header = ["TEAM_ID","OBJECT","MISSION_TIME","PACKET_CNT","ALTITUDE",
            "PRESSURE","SPEED","TEMP","VOLTAGE","HEADING","SOFTWARE_STATE"]
            writer = csv.DictWriter(csvfile, fieldnames=header)
            # writer.writeheader()
            writer.writerow({"TEAM_ID":6159,
                            "OBJECT": self.cansat.identifier,
                            "MISSION_TIME":self.cansat.telemetry_time, #self.cansat.mission_time,
                            "PACKET_CNT": self.cansat.packet_cnt + self.cansat.packet_cnt_glider,
                            "ALTITUDE":self.cansat.altitude[-1],
                            "PRESSURE":self.cansat.pressure[-1],
                            "SPEED":self.cansat.pitot[-1],
                            "TEMP": self.cansat.temp_outside[-1],
                            "VOLTAGE": self.cansat.voltage[-1],
                            "HEADING": self.cansat.heading[-1],
                            "SOFTWARE_STATE": self.cansat.flight_status})
        root.after(1000, self.write_to_csv, root)
