'''
Find distnace as the crow flies
SSS Sux
'''
import serial
import pynmea2
import math

port = '/dev/ttyS0'                                          #defines the serial port connected to
ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)    #creates a serial object

def searchDATA(data):
    #searches for $GPGGA in the GPS information
    dataOUT = ['0000000000000','0000000000000','0000000000000','0000000000000']
    if data.find(b'GGA') > 0:
        #library searches the data
        dataGPS = pynmea2.parse(data)
        #list of data outputted from the GPS
        dataOUT = [str(dataGPS.timestamp), str(dataGPS.lat),str(dataGPS.lat_dir), str(dataGPS.lon),str(dataGPS.lon_dir), str(dataGPS.altitude),str(dataGPS.altitude_units), str(dataGPS.num_sats) ]

    return dataOUT

def convert(list):
    dmsLAT = list[1]                                #Makes Strings from input
    dmsLON = list[3]

    dmsLATlist = [dmsLAT[0:2],dmsLAT[2:4],dmsLAT[5:11]]     #places them into proper lists
    dmsLONlist = [dmsLON[0:3],dmsLON[3:5],dmsLON[6:11]]
    if float(dmsLAT) > 0:
        print(dmsLATlist, dmsLONlist)

    LAT = float(dmsLATlist[0]) + (float(dmsLATlist[1])+float(dmsLATlist[2])/100000)/60  #puts them into full for Decimal Degrees
    LON = ((float(dmsLONlist[0]) + (float(dmsLONlist[1])+float(dmsLONlist[2])/100000)/60))*(-1)
    if LAT > 0:
        print(LAT, LON)
    return LAT,LON

def findDISTANCE(LAT, LON, initLAT = 40.11, initLON = -88.238, R=6371*10**3):     #defines a function that takes an initial lon and an initial lat R=radius of earth
    deltaLAT = abs(LAT - initLAT)
    deltaLON = abs(LON - initLON)
    if LAT > 0:
        print(deltaLAT, deltaLON)

    radLAT = [LAT*math.pi/180, initLAT*math.pi/180, deltaLAT*math.pi/180]   #switches to RADIANS
    radLON = deltaLON*math.pi/180

    a = (math.sin(radLAT[2]/2))**2+math.cos(radLAT[1])*math.cos(radLAT[0])*(math.sin(radLON/2))**2     #haversine formula
    c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    d = R*c
    if LAT > 0:
        print(a,c,d)

    return d

while True:
    if ser.in_waiting > 0:
        data = ser.readline()
        dataOUTPUT = searchDATA(data)
        print (type(dataOUTPUT))
        Latitude, Longitude = convert(dataOUTPUT)
        Distance = findDISTANCE(Latitude, Longitude)
        print(str(Distance)+ ' m')
