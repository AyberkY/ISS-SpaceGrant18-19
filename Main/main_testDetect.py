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

launch_detect_hysteresis = 5        #Launch detection hysteresis value in milliseconds
launch_detect_threshold = 1.5       #Launch detection threshold acceleration value in Gs
coast_detect_hysteresis = 5         #Coast detection hysteresis value in milliseconds
coast_detect_threshold = 0.5        #Coast detection threshold acceleration value in Gs

filename = str(datetime.datetime.now()) + ".txt"
filehandle = open(filename, 'w')

OLED = LED.LED('orange')
GLED = LED.LED('green')
BLED = LED.LED('blue')
BUZZER = LED.BUZZER(True)
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
state = 0

def gatherData():

    dataArray = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    dataArray[0] = time.time()
    dataArray[1] = state

###############__________GPS1__________###############

    try:
        gpsData = GPS1.readLocation()

        dataArray[2] = gpsData['lat']
        dataArray[3] = gpsData['lon']
        dataArray[4] = gpsData['altitude']
        dataArray[5] = gpsData['sats']

    except:
        dataArray[2] = 0
        dataArray[3] = 0
        dataArray[4] = 0
        dataArray[5] = 0

###############__________ADC1__________###############
    try:
        dataArray[6] = ADC1.read_voltage(0)
        dataArray[7] = ADC1.read_voltage(1)
        dataArray[8] = ADC1.read_voltage(2)

    except:
        dataArray[6] = 0
        dataArray[7] = 0
        dataArray[8] = 0

###############__________BARO1__________###############
    try:
        baro_pressure = BARO1.getPressure()
        baro_altitude, cTemp = BARO1.getData()

        dataArray[9] = baro_pressure
        dataArray[10] = baro_altitude
        dataArray[11] = cTemp

    except:
        dataArray[9] = 0
        dataArray[10] = 0
        dataArray[11] = 0

###############__________PITOT1__________###############
    try:
        pitot_pressure = PITOT1.getPressure()

        dataArray[12] = pitot_pressure

    except:
        dataArray[12] = 0

###############__________IMU1__________###############
    try:
        accelData = IMU1.readAccel()
        gyroData = IMU1.readGyro()

        dataArray[13] = accelData['x']
        dataArray[14] = accelData['y']
        dataArray[15] = accelData['z']
        dataArray[16] = gyroData['x']
        dataArray[17] = gyroData['y']
        dataArray[18] = gyroData['z']

    except:
        dataArray[13] = 0
        dataArray[14] = 0
        dataArray[15] = 0
        dataArray[16] = 0
        dataArray[17] = 0
        dataArray[18] = 0

    return dataArray

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

try:
    CAM1.start_recording('/home/pi/ISS-SpaceGrant18-19/Camera/' + filename + '.h264')
except:
    filehandle.write('COULD NOT BEGIN CAMERA RECORDING\n')

print("\n~~~~~~~~~~~ENTERING FLIGHT LOOP~~~~~~~~~~~\n")
filehandle.write("\n~~~~~~~~~~~ENTERING FLIGHT LOOP~~~~~~~~~~~\n")

state = 1   #Switch to PAD mode

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

filehandle.write("unix_timestamp,state,latitude,longitude,altitude,satellites,bat1,bat2,bat3,baro_pressure,baro_altitude,cTemp,pitot,mpu_acc_x,mpu_acc_y,mpu_acc_z,mpu_gyr_x,mpu_gyr_y,mpu_gyr_z\n")

filehandle.close()

launch_detect_possible = False
coast_detect_possible = False

try:
    while True:
        dataArray = gatherData()

        ########################################################
        ###############     LAUNCH DETECTION     ###############
        ########################################################

        if state == 1 and not launch_detect_possible and abs(dataArray[13]) > launch_detect_threshold:
            launch_detect_possible = True
            T0 = time.time() * 1000

        if state == 1 and launch_detect_possible and abs(dataArray[13]) < launch_detect_threshold:
            launch_detect_possible = False

        if state == 1 and launch_detect_possible and abs(dataArray[13]) > launch_detect_threshold:
            if ((time.time() * 1000) - T0) > launch_detect_hysteresis:
                state = 2
                BUZZER.setHigh()
                BLED.setHigh()
                time.sleep(0.5)
                BUZZER.setLow()

        ########################################################
        ###############      COAST DETECTION     ###############
        ########################################################

        if state == 2 and not coast_detect_possible and abs(dataArray[13]) < coast_detect_threshold:
            coast_detect_possible = True
            T0 = time.time() * 1000

        if state == 2 and coast_detect_possible and abs(dataArray[13]) > coast_detect_threshold:
            coast_detect_possible = False

        if state == 2 and coast_detect_possible and abs(dataArray[13]) < coast_detect_threshold:
            if ((time.time() * 1000) - T0) > coast_detect_hysteresis:
                state = 3
                BUZZER.setHigh()
                BLED.setHigh()
                time.sleep(0.5)
                BUZZER.setLow()

        try:
            filehandle = open(filename,'a')
            filehandle.write(str(dataArray) + '\n')
            filehandle.flush()
            filehandle.close()

        except:
            pass



except KeyboardInterrupt:
    filehandle.close()
    sys.exit()
