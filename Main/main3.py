import sys, time, datetime, picamera

sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/ADC')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Barometer')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/PITOT')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Camera')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/GPS')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/IMU/MPU9250')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/IMU/H3LIS331')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Memory')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Telemetry')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/LED')


import ADS1x15, mpl3115a2, pitotSensor, GPS, mpu9250, H3LIS331, RFM9X, LED

launch_detect_hysteresis = 15        #Launch detection hysteresis value in milliseconds
launch_detect_threshold = 1.5        #Launch detection threshold acceleration value in Gs
coast_detect_hysteresis = 30         #Coast detection hysteresis value in milliseconds
coast_detect_threshold = 0.5         #Coast detection threshold acceleration value in Gs
apogee_detect_hysteresis = 100       #Apogee detection hysteresis value in milliseconds
apogee_detect_threshold = 5          #Apogee detection threshold value in meters per second
max_drogue_speed = 28                #Maximum descent speed to be considered under droge parachute
max_main_speed = 70                  #Maximum main speed to be considered under main parachute
sep_detect_threshold = 1             #Seperation detection threshold acceleration value in Gs
sep_detect_hysteresis = 5            #Seperation detection hysteresis value in milliseconds

apogee_lockout = 10                  #Seconds after launch that apogee can be detected

h3_x_offset = 0.100180059205895       #H3LIS331DL X axis offset value
h3_y_offset = -0.8908169804986723     #H3LIS331DL Y axis offset value
h3_z_offset = 0.6617206335642285      #H3LIS331DL Z axis offset value

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

dataArray = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

def gatherData():

    dataArray[0] = time.time()

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
#                     (MPU9250)
    try:
        accelData = IMU1.readAccel()
        gyroData = IMU1.readGyro()

        dataArray[13] = -accelData['x']
        dataArray[14] = -accelData['y']
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

###############__________IMU2__________###############
#                    (H3LIS331DL)
    try:
        accelData2 = IMU2.read_accl()

        dataArray[20] = round((accelData2['x'] - h3_x_offset), 4)
        dataArray[21] = round((accelData2['y'] - h3_y_offset), 4)
        dataArray[22] = round((accelData2['z'] - h3_z_offset), 4)

    except:
        dataArray[20] = 0
        dataArray[21] = 0
        dataArray[22] = 0

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
    IMU2 = H3LIS331.H3LIS331DL()
    IMU2.select_datarate()
    IMU2.select_data_config()

except:
    print("COULD NOT CONNECT TO H3LIS331DL")
    filehandle.write('COULD NOT CONNECT TO H3LIS331DL\n')
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

try:
    PITOT1.calPressure()
    filehandle.write("\tPITOT OFFSET:" + str(PITOT1.offset))
    print("PITOT OFFSET:" + str(PITOT1.offset) + "\n")
except:
    print("\n~~~~~~~~~~~PITOT CALIBRATION FAILED~~~~~~~~~~~\n")

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

filehandle.write("unix_timestamp,state,latitude,longitude,altitude,satellites,bat1,bat2,bat3,baro_pressure,baro_altitude,cTemp,pitot,mpu_acc_x,mpu_acc_y,mpu_acc_z,mpu_gyr_x,mpu_gyr_y,mpu_gyr_z,mpu_roll,h3_acc_x,h3_acc_y,h3_acc_z,vertical_speed,sep_det\n")

filehandle.close()

dataArray = gatherData()

launch_detect_possible = False
coast_detect_possible = False
apogee_detect_possible = False
descent_detect_possible = False
descent_detected = False
sep_detect_possible = False
sep_detected = False
sep_detect_time = 0

boost_start_time = 0
boost_duration = 0
coast_start_time = 0
coast_duration = 0

max_acceleration = 0
max_vertical_speed = 0
max_altitude = 0
successfull_charge = 0
drogue_descent_velocity = 0
main_deployment_altitude = 0
main_descent_velocity = 0

last_transmission_time = time.time()

accel_velocity = 0
roll = 0

prev_time = time.time()
prev_altitude = dataArray[10]

dataArray = gatherData()
for i in range(5):
    dataArray = gatherData()
    telemArray = [max_acceleration,boost_duration,max_vertical_speed,coast_duration,max_altitude,successfull_charge,drogue_descent_velocity,main_deployment_altitude,main_descent_velocity,dataArray[2],dataArray[3],dataArray[4],0]
    TELEM1.send(bytes(str(telemArray), "utf-8"))
print("initial send")

try:
    while True:
        dataArray = gatherData()

        ########################################################
        ###############   ONBOARD CALCULATIONS   ###############
        ########################################################

        roll += (dataArray[16] * (time.time() - prev_time))
        dataArray[19] = round(roll, 4)
        # print("Roll: " + str(roll))

        vertical_speed = round((dataArray[10] - prev_altitude) / (time.time() - prev_time), 4)
        prev_altitude = dataArray[10]
        if state > 1 and vertical_speed != 0.0:
            dataArray[23] = vertical_speed
        # print("Vertical Speed: " + str(dataArray[23]) + "\t" + "Altitude" + str(dataArray[10]))

        # accel_velocity += round((dataArray[13] * (time.time() - prev_time)), 4)
        # print("\t\t\t\t\tAccel Speed: " + str(accel_velocity) + "m/s")

        if state >= 1:
            dataArray[0] -= boost_start_time

        prev_time = time.time()

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
                boost_start_time = dataArray[0]
                dataArray[0] = 0.0
                print("BOOST DETECTED")

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
                coast_start_time = time.time()
                boost_duration = coast_start_time - boost_start_time
                print("COAST DETECTED")

        ########################################################
        ###############     APOGEE DETECTION     ###############
        ########################################################

        if state == 3 and not apogee_detect_possible and abs(dataArray[23]) < apogee_detect_threshold and dataArray[0] > apogee_lockout:
            apogee_detect_possible = True
            T0 = time.time() * 1000

        if state == 3 and apogee_detect_possible and abs(dataArray[23]) > apogee_detect_threshold:
            apogee_detect_possible = False

        if state == 3 and apogee_detect_possible and abs(dataArray[23]) < apogee_detect_threshold:
            if ((time.time() * 1000) - T0) > apogee_detect_hysteresis:
                state = 4
                coast_duration = time.time() - coast_start_time
                print("APOGEE DETECTED")

        ########################################################
        ###############  DESCENT CLASSIFICATION  ###############
        ########################################################

        # if state == 4 and not descent_detect_possible and abs(vertical_speed) > apogee_detect_threshold:
        #     descent_detect_possible = True
        #     T0 = time.time() * 1000
        #
        # if state == 4 and descent_detect_possible and abs(vertical_speed) < apogee_detect_threshold:
        #     descent_detect_possible = False
        #
        # if state == 4 and apogee_detect_possible and abs(vertical_speed) > apogee_detect_threshold:
        #     if ((time.time() * 1000) - T0) > apogee_detect_hysteresis:
        #         descent_detected = True

        if state == 4 and dataArray[10] >= 22:
            descent_detected = True
            print("DESCENT DETECTED")

        if descent_detected:
            if abs(dataArray[23]) < max_main_speed:
                state = 6
                main_deployment_altitude = dataArray[10]
                print("DESCENDING UNDER MAIN")
            elif abs(dataArray[23]) > max_main_speed and abs(dataArray[23]) < max_drogue_speed:
                state = 5
                print("DESCENDING UNDER DROGUE")
            else:
                state = 7
                print("BALLISTIC")

        #########################################################
        ############### SEPERATION CLASSIFICATION ###############
        #########################################################

        if state == 4 and not sep_detect_possible and abs(dataArray[13]) > sep_detect_threshold:
            sep_detect_possible = True
            T0_2 = time.time() * 1000

        if state == 4 and sep_detect_possible and abs(dataArray[13]) < sep_detect_threshold:
            sep_detect_possible = False

        if state == 4 and sep_detect_possible and abs(dataArray[13]) > sep_detect_threshold:
            if ((time.time() * 1000) - T0_2) > sep_detect_hysteresis:
                sep_detected = True
                if abs(dataArray[23]) < 5:
                    dataArray[24] = 1
                    successfull_charge = 1
                    print("SUCCESFULL PRIMARY CHARGE DETECTED")
                else:
                    dataArray[24] = 2
                    successfull_charge = 2
                    print("SUCCESSFUL SECONDARY CHARGE DETECTED")

        #########################################################
        ####################### TELEMETRY #######################
        #########################################################

        if state == 2:
            if dataArray[23] > max_vertical_speed:
                max_vertical_speed = dataArray[23]

            if dataArray[13] > max_acceleration:
                max_acceleration = dataArray[13]

        if state == 3 or state == 4:
            if dataArray[10] > max_altitude:
                max_altitude = dataArray[10]

        if state == 5:
            drogue_descent_velocity = dataArray[23]

        if state == 6:
            main_descent_velocity = dataArray[23]

        if state == 5 or state == 6 or state == 7:
        # if state == 4:
            if (time.time() - last_transmission_time) > 2.0:
                telemArray = [max_acceleration,boost_duration,max_vertical_speed,coast_duration,max_altitude,dataArray[24],drogue_descent_velocity,main_deployment_altitude,main_descent_velocity,dataArray[2],dataArray[3],dataArray[4]]
                TELEM1.send(bytes(str(telemArray), "utf-8"))
                last_transmission_time = time.time()
                print("sending data")

        dataArray[1] = state

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
