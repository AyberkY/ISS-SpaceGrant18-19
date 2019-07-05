import sys, time, datetime, picamera

sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/ADC')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Barometer')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/PITOT')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Camera')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/GPS')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/IMU/MPU9250')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Memory')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Telemetry')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/LED')


import ADS1x15, mpl3115a2, pitotSensor, GPS, mpu9250, RFM9X, LED

filename = str(datetime.datetime.now()) + ".txt"
filehandle = open(filename, 'w')

OLED = LED.LED('orange')
GLED = LED.LED('green')
BLED = LED.LED('blue')
BUZZER = LED.BUZZER(False)
OLED.setLow()
GLED.setLow()
BLED.setLow()
BUZZER.setLow()

time.sleep(1)

OLED.setHigh()
BUZZER.setHigh()
time.sleep(0.05)
BUZZER.setLow()
time.sleep(0.3)
GLED.setHigh()
BUZZER.setHigh()
time.sleep(0.05)
BUZZER.setLow()
time.sleep(0.3)
BLED.setHigh()
BUZZER.setHigh()
time.sleep(0.05)
BUZZER.setLow()
time.sleep(1)
OLED.setLow()
GLED.setLow()
BLED.setLow()

Initialization_Error = False

"""
States of flight computer:
0 - INITIALIZATION
1 - PAD / IDLE
2 - BOOST
3 - COAST
4 - APOGEE
5 - UNDER DROGUE
6 - UNDER MAIN
7 - BALLISTIC
"""
State = 0

initializations = []

print("\n~~~~~~~~~~~INITIALIZING SUB-SYSTEMS~~~~~~~~~~~\n")
filehandle.write("\n~~~~~~~~~~~INITIALIZING SUB-SYSTEMS~~~~~~~~~~~\n")

try:
    GPS1 = GPS.GPS()
except:
    print("COULD NOT CONNECT TO GPS")
    filehandle.write('COULD NOT CONNECT TO GPS\n')
    Initialization_Error = True

try:
    ADC1 = ADS1x15.ADS1115()
except:
    print("COULD NOT CONNECT TO ADC")
    filehandle.write('COULD NOT CONNECT TO ADC\n')
    Initialization_Error = True

try:
    BARO1 = mpl3115a2.Barometer()
except:
    print("COULD NOT CONNECT TO BAROMETER")
    filehandle.write('COULD NOT CONNECT TO BAROMETER\n')
    Initialization_Error = True

try:
    PITOT1 = pitotSensor.PITOT()
except:
    print("COULD NOT CONNECT TO PITOT SENSOR")
    filehandle.write('COULD NOT CONNECT TO PITOT SENSOR\n')
    Initialization_Error = True

try:
    IMU1 = mpu9250.MPU9250()
except:
    print("COULD NOT CONNECT TO MPU9250")
    filehandle.write('COULD NOT CONNECT TO MPU9250\n')
    Initialization_Error = True

try:
    TELEM1 = RFM9X.RFM9X()
except:
    print("COULD NOT CONNECT TO TELEMETRY")
    filehandle.write('COULD NOT CONNECT TO TELEMETRY\n')
    Initialization_Error = True

try:
    CAM1 = picamera.PiCamera()
except:
    print("COULD NOT CONNECT TO CAMERA")
    filehandle.write('COULD NOT CONNECT TO CAMERA\n')
    Initialization_Error = True


print("\n~~~~~~~~~~~INITIALIZATION COMPLETE~~~~~~~~~~~\n")
filehandle.write("\n~~~~~~~~~~~INITIALIZATION COMPLETE~~~~~~~~~~~\n")

for i in range(5):
    OLED.setHigh()
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

print("\n~~~~~~~~~~~CALIBRATING PITOT SENSOR~~~~~~~~~~~\n")
filehandle.write("\n~~~~~~~~~~~CALIBRATING PITOT SENSOR~~~~~~~~~~~\n")

PITOT1.calPressure()
filehandle.write("\tPITOT OFFSET:" + str(PITOT1.offset))
print("PITOT OFFSET:" + str(PITOT1.offset) + "\n")

print("\n~~~~~~~~~~~STARTING VIDEO RECORDING~~~~~~~~~~~\n")
filehandle.write("\n~~~~~~~~~~~STARTING VIDEO RECORDING~~~~~~~~~~~\n")

CAM1.start_recording('/home/pi/ISS-SpaceGrant18-19/Camera/' + filename + '.h264')

print("\n~~~~~~~~~~~ENTERING FLIGHT LOOP~~~~~~~~~~~\n")
filehandle.write("\n~~~~~~~~~~~ENTERING FLIGHT LOOP~~~~~~~~~~~\n")

if Initialization_Error:
    OLED.setHigh()
    BUZZER.setHigh()
    time.sleep(0.2)
    BUZZER.setLow()
    time.sleep(0.1)
    BUZZER.setHigh()
    time.sleep(0.2)
    BUZZER.setLow()
    time.sleep(0.1)
else:
    BUZZER.setHigh()
    time.sleep(0.02)
    BUZZER.setLow()
    time.sleep(0.1)
    BUZZER.setHigh()
    time.sleep(0.02)
    BUZZER.setLow()
    time.sleep(0.1)
    BUZZER.setHigh()
    time.sleep(0.02)
    BUZZER.setLow()

GLED.setHigh()

filehandle.write("hour,minute,second,microsecond,state,latitude,longitude,altitude,satellites,bat1,bat2,bat3,baro_pressure,baro_altitude,cTemp,pitot,mpu_acc_x,mpu_acc_y,mpu_acc_z,mpu_gyr_x,mpu_gyr_y,mpu_gyr_z\n")

filehandle.close()
try:
    while True:
        filehandle = open(filename,'a')

        dataArray = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        dataArray[0] = datetime.datetime.now().hour
        dataArray[1] = datetime.datetime.now().minute
        dataArray[2] = datetime.datetime.now().second
        dataArray[3] = datetime.datetime.now().microsecond
        dataArray[4] = state

    ###############__________GPS1__________###############

        try:
            gpsData = GPS1.readLocation()

            dataArray[5] = gpsData['lat']
            dataArray[6] = gpsData['lon']
            dataArray[7] = gpsData['altitude']
            dataArray[8] = gpsData['sats']

        except:
            dataArray[5] = 0
            dataArray[6] = 0
            dataArray[7] = 0
            dataArray[8] = 0

    ###############__________ADC1__________###############
        try:
            dataArray[9] = ADC1.read_adc(0)
            dataArray[10] = ADC1.read_adc(1)
            dataArray[11] = ADC1.read_adc(2)

        except:
            dataArray[9] = 0
            dataArray[10] = 0
            dataArray[11] = 0

    ###############__________BARO1__________###############
        try:
            baro_pressure = BARO1.getPressure()
            baro_altitude, cTemp = BARO1.getData()

            dataArray[12] = baro_pressure
            dataArray[13] = baro_altitude
            dataArray[14] = cTemp

        except:
            dataArray[12] = 0
            dataArray[13] = 0
            dataArray[14] = 0

    ###############__________PITOT1__________###############
        try:
            pitot_pressure = PITOT1.getPressure()

            dataArray[15] = pitot_pressure

        except:
            dataArray[15] = 0

    ###############__________IMU1__________###############
        try:
            accelData = IMU1.readAccel()
            gyroData = IMU1.readGyro()

            dataArray[16] = accelData['x']
            dataArray[17] = accelData['y']
            dataArray[18] = accelData['z']
            dataArray[19] = gyroData['x']
            dataArray[20] = gyroData['y']
            dataArray[21] = gyroData['z']

        except:
            dataArray[16] = 0
            dataArray[17] = 0
            dataArray[18] = 0
            dataArray[19] = 0
            dataArray[20] = 0
            dataArray[21] = 0

    ###############_________TELEMETRY_________###############
        try:
            TELEM1.send(dataArray)

    ###############__________WRITE TO SD__________###############
        filehandle.write(str(dataArray) + '\n')
        filehandle.flush()

except KeyboardInterrupt:
    filehandle.close()
    sys.exit()
