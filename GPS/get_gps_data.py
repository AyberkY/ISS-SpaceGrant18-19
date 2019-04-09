from serial import Serial # Import the Serial class only from the pyserial library.
import pynmea2

port = '/dev/ttyS0'                       #defines the serial port connected to
ser = Serial(port, baudrate = 9600, timeout = 0.5)    #creates a serial object

def searchDATA(data):
    dataOUT = ''
    if data.find(b'GGA') > 0:                #searches for $GPGGA in the GPS information
        dataGPS = pynmea2.parse(data.decode('utf-8'))       #library does this stuff somehow
        dataOUT = [str(dataGPS.timestamp), str(dataGPS.lat) + ' ' + str(dataGPS.lat_dir), str(dataGPS.lon) + ' ' + str(dataGPS.lon_dir), str(dataGPS.altitude) + ' ' + str(dataGPS.altitude_units), str(dataGPS.num_sats) + ' satellites']
    return dataOUT

while True:
    if ser.in_waiting > 0:                #checks if there is new data in the input buffer.
        data = ser.readline()               #reads fron the input buffer.
        dataOUT = searchDATA(data)
        print(dataOUT)
        ser.reset_input_buffer()           #flushes the input buffer.
