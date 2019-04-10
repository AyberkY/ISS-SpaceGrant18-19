import sys, time, datetime

sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/ADC')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Barometer')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Camera')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/GPS')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/IMU/MPU9250')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Memory')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Telemetry')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/LED')


import ADS1x15, mpl3115a2, GPS, mpu9250, RFM9X, LED

filename = str(datetime.datetime.now())
filehandle = open(filename, 'w+')


OLED = LED.LED('orange')
GLED = LED.LED('green')
BLED = LED.LED('blue')
OLED.setLow()
GLED.setLow()
BLED.setLow()

time.sleep(1)

OLED.setHigh()
time.sleep(0.3)
GLED.setHigh()
time.sleep(0.3)
BLED.setHigh()
time.sleep(1)
OLED.setLow()
GLED.setLow()
BLED.setLow()

print("\n~~~~~~~~~~~INITIALIZING SUB-SYSTEMS~~~~~~~~~~~\n")
filehandle.write("\n~~~~~~~~~~~INITIALIZING SUB-SYSTEMS~~~~~~~~~~~\n")

try:
    GPS1 = GPS.GPS()
except:
    print("COULD NOT CONNECT TO GPS")
    filehandle.write('COULD NOT CONNECT TO GPS\n')

try:
    ADC1 = ADS1x15.ADS1115()
except:
    print("COULD NOT CONNECT TO ADC")
    filehandle.write('COULD NOT CONNECT TO ADC\n')

try:
    BARO1 = mpl3115a2.Barometer()
except:
    print("COULD NOT CONNECT TO BAROMETER")
    filehandle.write('COULD NOT CONNECT TO BAROMETER\n')

try:
    IMU1 = mpu9250.MPU9250()
except:
    print("COULD NOT CONNECT TO MPU9250")
    filehandle.write('COULD NOT CONNECT TO MPU9250\n')

try:
    TELEM1 = RFM9X.RFM9X()
except:
    print("COULD NOT CONNECT TO TELEMETRY")
    filehandle.write('COULD NOT CONNECT TO TELEMETRY\n')

print("\n~~~~~~~~~~~INITIALIZATION COMPLETE~~~~~~~~~~~\n")
filehandle.write("\n~~~~~~~~~~~INITIALIZATION COMPLETE~~~~~~~~~~~\n")

for i in range(5):
    OLED.setLow()
    BLED.setLow()
    time.sleep(0.1)
    OLED.setLow()
    BLED.setHigh()
    time.sleep(0.1)

OLED.setLow()
BLED.setLow()
GLED.setLow()

time.sleep(0.5)

print("\n~~~~~~~~~~~CALIBRATING IMU1~~~~~~~~~~~\n")
filehandle.write("\n~~~~~~~~~~~CALIBRATING IMU1~~~~~~~~~~~\n")

BLED.setHigh()
gyroOffsets = IMU1.calGyro()
filehandle.write("IMU1 OFFSETS:\n")
filehandle.write("\tGX_OFFSET:" + str(gyroOffsets[0]) + "\n")
filehandle.write("\tGY_OFFSET:" + str(gyroOffsets[1]) + "\n")
filehandle.write("\tGZ_OFFSET:" + str(gyroOffsets[2]) + "\n\n")
BLED.setLow()

print("\n~~~~~~~~~~~ENTERING FLIGHT LOOP~~~~~~~~~~~\n")
filehandle.write("\n~~~~~~~~~~~ENTERING FLIGHT LOOP~~~~~~~~~~~\n")

GLED.setHigh()

filehandle.write("hour,minute,second,microsecond,latitude,longitude,altitude,satellites,bat1,bat2,bat3,baro_pressure,baro_altitude,cTemp,mpu_acc_x,mpu_acc_y,mpu_acc_z,mpu_gyr_x,mpu_gyr_y,mpu_gyr_z\n")

try:
    while True:
        dataArray = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        dataArray[0] = datetime.datetime.now().hour
        dataArray[1] = datetime.datetime.now().minute
        dataArray[2] = datetime.datetime.now().second
        dataArray[3] = datetime.datetime.now().microsecond

    ###############__________GPS1__________###############
        try:
            gpsData = GPS1.readLocation()

            dataArray[4] = gpsData['lat']
            dataArray[5] = gpsData['lon']
            dataArray[6] = gpsData['altitude']
            dataArray[7] = gpsData['sats']

        except:
            dataArray[4] = 0
            dataArray[5] = 0
            dataArray[6] = 0
            dataArray[7] = 0

    ###############__________ADC1__________###############
        try:
            dataArray[8] = ADC1.read_adc(0)
            dataArray[9] = ADC1.read_adc(1)
            dataArray[10] = ADC1.read_adc(2)

        except:
            dataArray[8] = 0
            dataArray[9] = 0
            dataArray[10] = 0

    ###############__________BARO1__________###############
        try:
            baro_pressure = BARO1.getPressure()
            baro_altitude, cTemp = BARO1.getData()

            dataArray[11] = baro_pressure
            dataArray[12] = baro_altitude
            dataArray[13] = cTemp

        except:
            dataArray[11] = 0
            dataArray[12] = 0
            dataArray[13] = 0

    ###############__________IMU1__________###############
        try:
            accelData = IMU1.readAccel()
            gyroData = IMU1.readGyro()

            dataArray[14] = accelData['x']
            dataArray[15] = accelData['y']
            dataArray[16] = accelData['z']
            dataArray[17] = gyroData['x']
            dataArray[18] = gyroData['y']
            dataArray[19] = gyroData['z']

        except:
            dataArray[14] = 0
            dataArray[15] = 0
            dataArray[16] = 0
            dataArray[17] = 0
            dataArray[18] = 0
            dataArray[19] = 0

    ###############__________WRITE TO SD__________###############
        filehandle.write(str(dataArray) + '\n')

    ###############_________TELEMETRY_________###############

except KeyboardInterrupt:
    filehandle.close()
