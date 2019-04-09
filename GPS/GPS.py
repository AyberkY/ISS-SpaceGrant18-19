import serial
import pynmea2
import math
from time import sleep



class GPS:

    def __init__(self, port ='/dev/ttyS0', baudrate = 9600, biteSize = 8):
        self.ser = serial.Serial(port, baudrate, biteSize)
        self.HOME_LAT = 0
        self.HOME_LON = 0
        self.CUR_LAT = 0
        self.CUR_LON = 0
        self.HOME_LOCATED = False
        self.HOME_TIME = -1
        self.R = 6371*10**3
        self.ALT = 0

        while not self.ser.in_waiting > 0:
            sleep(5)

    def readLocation(self):
        #searches for $GPGGA in the GPS information
        dataOUT = [0,0,0,0,0,0,0,0] #forces the program to pass trhough something that isn't a none type
        if self.ser.in_waiting > 0:
            data = self.ser.readline()
            self.ser.flush() #Flushes the input


            if data.find(b'GGA') > 0:
                try:
                    #library searches the data
                    dataGPS = pynmea2.parse(data.decode('utf-8'))
                    #list of data outputted from the GPS
                    dataOUT = [str(dataGPS.timestamp), str(dataGPS.lat), str(dataGPS.lat_dir), str(dataGPS.lon), str(dataGPS.lon_dir), str(dataGPS.altitude), str(dataGPS.altitude_units), str(dataGPS.num_sats)]

                    dmsLAT = dataOUT[1]                                #Makes Strings from input
                    dmsLON = dataOUT[3]
                    dmsLATlist = [dmsLAT[0:2],dmsLAT[2:4],dmsLAT[5:11]]     #places them into proper lists
                    dmsLONlist = [dmsLON[0:3],dmsLON[3:5],dmsLON[6:11]]
                    #if float(dmsLAT) > 0:
                    #    print(dmsLATlist, dmsLONlist)
                    if not self.HOME_LOCATED:
                        self.HOME_LAT = round(float(dmsLATlist[0]) + (float(dmsLATlist[1]) + float(dmsLATlist[2])/100000)/60,5)  #puts them into full for Decimal Degrees
                        self.HOME_LON = round((float(dmsLONlist[0]) + (float(dmsLONlist[1]) + float(dmsLONlist[2])/100000)/60)*(-1),5)
                        self.HOME_TIME = dataGPS.timestamp
                        self.HOME_LOCATED = True
                        self.ALT = dataGPS.altitude
                    else:
                        self.CUR_LAT = round(float(dmsLATlist[0]) + (float(dmsLATlist[1]) + float(dmsLATlist[2])/100000)/60,5)  #puts them into full for Decimal Degrees
                        self.CUR_LON = round((float(dmsLONlist[0]) + (float(dmsLONlist[1]) + float(dmsLONlist[2])/100000)/60)*(-1),5)
                        self.ALT = dataGPS.altitude

                except:
                    data = ''

        return {"lat":self.CUR_LAT, "lon":self.CUR_LON, "timestamp":dataOUT[0], "sats":dataOUT[7], "altitude":dataOUT[5]}

    def homeLocation(self):
        return {"lat": self.HOME_LAT, "lon": self.HOME_LON, "time": self.HOME_TIME}

    def distanceFromHome(self):
        currLocation = self.readLocation()
        deltaLAT = abs(currLocation['lat'] - self.HOME_LAT)
        deltaLON = abs(currLocation['lon'] - self.HOME_LON)
        radLAT = [currLocation['lat']*math.pi/180, self.HOME_LAT*math.pi/180, deltaLAT*math.pi/180]   #switches to RADIANS
        radLON = deltaLON*math.pi/180

        a = (math.sin(radLAT[2]/2))**2+math.cos(radLAT[1])*math.cos(radLAT[0])*(math.sin(radLON/2))**2     #haversine formula
        c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))
        distance = round(self.R*c,4)
        return distance
