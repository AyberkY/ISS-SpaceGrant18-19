import serial
import pynmea2
import math
from time import sleep



class GPS:

    def __init__(self, port ='/dev/ttyS0', baudrate = 9600, timeout = 0.5):
        self.ser = serial.Serial(port, baudrate, timeout)
        self.HOME_LAT = 0
        self.HOME_LON = 0
        self.CUR_LAT = 0
        self.CUR_LON = 0
        self.HOME_LOCATED = False
        self.HOME_TIME = -1

        while not ser.in_waiting > 0:
            sleep(5)

    def readLocation(self):
        #searches for $GPGGA in the GPS information

        if ser.in_waiting > 0:
            data = ser.readline()

            dataOUT = ['0000000000000','0000000000000','0000000000000','0000000000000'] #forces the program to pass trhough something that isn't a none type
            if data.find('GGA') > 0:
                #library searches the data
                dataGPS = pynmea2.parse(data)
                #list of data outputted from the GPS
                dataOUT = [str(dataGPS.timestamp), str(dataGPS.lat),str(dataGPS.lat_dir), str(dataGPS.lon),str(dataGPS.lon_dir), str(dataGPS.altitude),str(dataGPS.altitude_units), str(dataGPS.num_sats) ]

                dmsLAT = dataOUT[1]                                #Makes Strings from input
                dmsLON = dataOUT[3]
                dmsLATlist = [dmsLAT[0:2],dmsLAT[2:4],dmsLAT[5:11]]     #places them into proper lists
                dmsLONlist = [dmsLON[0:3],dmsLON[3:5],dmsLON[6:11]]
                #if float(dmsLAT) > 0:
                #    print(dmsLATlist, dmsLONlist)
                if not HOME_LOCATED:
                    self.HOME_LAT = float(dmsLATlist[0]) + (float(dmsLATlist[1])+float(dmsLATlist[2])/100000)/60  #puts them into full for Decimal Degrees
                    self.HOME_LON = ((float(dmsLONlist[0]) + (float(dmsLONlist[1])+float(dmsLONlist[2])/100000)/60))*(-1)
                    self.HOME_TIME = dataOUT = dataGPS.timestamp
                    self.HOME_LOCATED = True
                else:
                    self.CUR_LAT = float(dmsLATlist[0]) + (float(dmsLATlist[1])+float(dmsLATlist[2])/100000)/60  #puts them into full for Decimal Degrees
                    self.CUR_LON = ((float(dmsLONlist[0]) + (float(dmsLONlist[1])+float(dmsLONlist[2])/100000)/60))*(-1)

                return {"lat":self.CUR_LAT, "lon":self.CUR_LON}

    def homeLocation(self):
        return {"lat": self.HOME_LAT, "lon": self.HOME_LON, "time": self.HOME_TIME}

    def distanceFromHome(self):
        currLocation = self.readLocation
        deltaLAT = abs(currLocation['lat'] - self.HOME_LAT)
        deltaLON = abs(currLocation['lon'] - self.HOME_LON)
        radLAT = [currLocation['lat']*math.pi/180, self.HOME_LAT*math.pi/180, deltaLAT*math.pi/180]   #switches to RADIANS
        radLON = deltaLON*math.pi/180

        a = (math.sin(radLAT[2]/2))**2+math.cos(radLAT[1])*math.cos(radLAT[0])*(math.sin(radLON/2))**2     #haversine formula
        c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))
        distance = R*c
        return distance