import serial
import pynmea2

port = '/dev/ttyS0'                       #defines the serial port connected to
ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)    #creates a serial object

def searchDATA(data):
    dataOUT = ''
    if data.find('GGA') > 0:                #searches for $GPGGA in the GPS information
        dataGPS = pynmea2.parse(data)       #library does this stuff somehow
        dataOUT = [str(dataGPS.timestamp), str(dataGPS.lat) + ' ' + str(dataGPS.lat_dir), str(dataGPS.lon) + ' ' + str(dataGPS.lon_dir), str(dataGPS.altitude) + ' ' + str(dataGPS.altitude_units)]
    print( dataOUT )
    return dataOUT

while 1==1:                                 #keeps searching the data
    data = ser.readline()
    searchDATA(data)
