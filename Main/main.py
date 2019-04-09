import sys, time, datetime

sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/ADC')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Barometer')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Camera')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/GPS')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/IMU/MPU9250')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Memory')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Telemetry')

import ADS1x15, mpl3115a2, GPS, mpu9250, RFM9X

filename = str(datetime.datetime.now())
filehandle = open(filename, 'w+')

print("\n~~~~~~~~~~~INITIALIZING SENSORS~~~~~~~~~~~\n")
filehandle.write("\n~~~~~~~~~~~INITIALIZING SENSORS~~~~~~~~~~~\n")

try:
    GPS1 = GPS.GPS()
except:
    print("COULD NOT CONNECT TO GPS")

try:
    ADC1 = ADS1x15.ADS1115()
except:
    print("COULD NOT CONNECT TO ADC")

try:
    BARO1 = mpl3115a2.Barometer()
except:
    print("COULD NOT CONNECT TO BAROMETER")

try:
    IMU1 = mpu9250.MPU9250()
except:
    print("COULD NOT CONNECT TO MPU9250")

try:
    TELEM1 = RFM9X.RFM9X()
except:
    print("COULD NOT CONNECT TO TELEMETRY")

print("\n~~~~~~~~~~~INITIALIZATION COMPLETE~~~~~~~~~~~\n")
filehandle.write("\n~~~~~~~~~~~INITIALIZATION COMPLETE~~~~~~~~~~~\n")

time.sleep(0.5)

print("\n~~~~~~~~~~~ENTERING FLIGHT LOOP~~~~~~~~~~~\n")
filehandle.write("\n~~~~~~~~~~~ENTERING FLIGHT LOOP~~~~~~~~~~~\n")

filehandle.write("timestamp,latitude,longitude,altitude,satellites,bat1,bat2,bat3,baro_pressure,baro_altitude,cTemp,mpu_acc_x,mpu_acc_y,mpu_acc_z,mpu_gyr_x,mpu_gyr_y,mpu_gyr_z\n")

try:
    while True:
        dataArray = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        dataArray[0] = str(datetime.datetime.now().time())

    ###############__________GPS1__________###############
        try:
            gpsData = GPS1.readLocation()

            dataArray[1] = gpsData['lat']
            dataArray[2] = gpsData['lon']
            dataArray[3] = gpsData['altitude']
            dataArray[4] = gpsData['sats']

        except:
            dataArray[1] = 0
            dataArray[2] = 0
            dataArray[3] = 0
            dataArray[4] = 0

    ###############__________ADC1__________###############
        try:
            dataArray[5] = ADC1.read_adc(0)
            dataArray[6] = ADC1.read_adc(1)
            dataArray[7] = ADC1.read_adc(2)

        except:
            dataArray[5] = 0
            dataArray[6] = 0
            dataArray[7] = 0

    ###############__________BARO1__________###############
        try:
            baro_pressure = BARO1.getPressure()
            baro_altitude, cTemp = BARO1.getData()

            dataArray[8] = baro_pressure
            dataArray[9] = baro_altitude
            dataArray[10] = cTemp

        except:
            dataArray[8] = 0
            dataArray[9] = 0
            dataArray[10] = 0

    ###############__________IMU1__________###############
        try:
            accelData = IMU1.readAccel()
            gyroData = IMU1.readGyro()

            dataArray[11] = accelData['x']
            dataArray[12] = accelData['y']
            dataArray[13] = accelData['z']
            dataArray[14] = gyroData['x']
            dataArray[15] = gyroData['y']
            dataArray[16] = gyroData['z']

        except:
            dataArray[11] = 0
            dataArray[12] = 0
            dataArray[13] = 0
            dataArray[14] = 0
            dataArray[15] = 0
            dataArray[16] = 0

    ###############__________WRITE TO SD__________###############
        filehandle.write(str(dataArray) + '\n')

    ###############_________TELEMETRY_________###############

except KeyboardInterrupt:
    filehandle.close()
