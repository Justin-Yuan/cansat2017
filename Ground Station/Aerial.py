from random import randint, uniform
import datetime
import helpers
import csv
class Cansat(object):
    """ Cansat class to encapsulate shared variables and functions
    """
    def __init__(self):
        self.packet_cnt = 0
        self.altitude = [0.0]
        self.mission_time = str(datetime.datetime.now())[14:19]
        self.pressure = [0.0] # glider only
        self.pitot = [0.0]
        self.temp_outside = [0.0]
        self.voltage = [0.0]  # solar power voltage for glider
        self.heading = [0.0]  # glider only
        self.gps_lat = [0.0]
        self.gps_long = [0.0]
        self.gps_alt = [0.0]
        self.gps_num = 0      # what is this
        self.gps_speed = [0.0]
        self.flight_status = 0
        self.identifier = "CONTAINER"


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
        self.csv_test = True
        self.file_name = file_name

    def serial_update_write(self, root):
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
            angle = randint(-180,180) #12
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

        # TO-DO: verify the data_list fields
        elif self.ser_connected:   # TODO : target object needs to be fixed 
            data = self.ser.readline()
            data_list = data.split(",")
            #listbox.insert(0, ["TEST ",data_list])
            print data_list
            if len(data_list) == 8:
                #listbox.insert(0, ["TEST ",data_list])
                target.packet_cnt += 1
                for i in range(0,8):
                    if (data_list[i] == ""):
                        data_list[i] = str(000)

                    try:
                        float(data_list[i])
                    except:
                        data_list[i] = str(000)

                self.cansat.pitot.append(float(data_list[3]))
                self.cansat.altitude.append(float(data_list[4]))
                self.cansat.temp_outside.append(float(data_list[5]))
                self.cansat.voltage.append(float(data_list[6]))
                # target.heading.append(float(data_list[7]))
                self.cansat.flight_status = float(data_list[7])

        root.after(1000, self.serial_update_write, root)

    def write_to_csv(self, root): # writes in parallel with the serial update
        with open(self.file_name, 'aw+') as csvfile:
            header = ["6159","OBJECT","MISSION_TIME","PACKET_CNT","ALTITUDE",
            "PRESSURE","SPEED","TEMP","VOLTAGE","HEADING","SOFTWARE_STATE"]
            writer = csv.DictWriter(csvfile, fieldnames=header)
            # writer.writeheader()
            writer.writerow({"6159":6159,
                            "OBJECT": self.cansat.identifier,
                            "MISSION_TIME":self.cansat.mission_time,
                            "PACKET_CNT": self.cansat.packet_cnt,
                            "ALTITUDE":self.cansat.altitude[-1],
                            "PRESSURE":self.cansat.pressure[-1],
                            "SPEED":self.cansat.pitot[-1],
                            "TEMP": self.cansat.temp_outside[-1],
                            "VOLTAGE": self.cansat.voltage[-1],
                            "HEADING": self.cansat.heading[-1],
                            "SOFTWARE_STATE": self.cansat.flight_status})
        root.after(1000, self.write_to_csv, root)
