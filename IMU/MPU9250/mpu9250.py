# Dedicated to my beloved Professor
# May he rest gayly
#02/22/2019

import smbus
import time
import math

## MPU9250 Default I2C slave address
SLAVE_ADDRESS        = 0x69
## Magnetometer: AK8963 I2C slave address
AK8963_SLAVE_ADDRESS = 0x0C
## Device id
DEVICE_ID            = 0x71

''' MPU-9250 Register Addresses '''
SMPLRT_DIV     = 0x19 #sample rate driver
CONFIG         = 0x1A #configuration
GYRO_CONFIG    = 0x1B #gyroscope configuration
ACCEL_CONFIG   = 0x1C #acceleration configuration
ACCEL_CONFIG_2 = 0x1D
LP_ACCEL_ODR   = 0x1E
WOM_THR        = 0x1F
FIFO_EN        = 0x23
I2C_MST_CTRL   = 0x24
I2C_MST_STATUS = 0x36
INT_PIN_CFG    = 0x37
INT_ENABLE     = 0x38
INT_STATUS     = 0x3A
ACCEL_OUT      = 0x3B
TEMP_OUT       = 0x41
GYRO_OUT       = 0x43

I2C_MST_DELAY_CTRL = 0x67
SIGNAL_PATH_RESET  = 0x68
MOT_DETECT_CTRL    = 0x69
USER_CTRL          = 0x6A
PWR_MGMT_1         = 0x6B
PWR_MGMT_2         = 0x6C
FIFO_R_W           = 0x74
WHO_AM_I           = 0x75

## Gyro Full Scale Select 250dps
GFS_250  = 0x00
## Gyro Full Scale Select 500dps
GFS_500  = 0x01
## Gyro Full Scale Select 1000dps
GFS_1000 = 0x02
## Gyro Full Scale Select 2000dps
GFS_2000 = 0x03
## Accel Full Scale Select 2G
AFS_2G   = 0x00
## Accel Full Scale Select 4G
AFS_4G   = 0x01
## Accel Full Scale Select 8G
AFS_8G   = 0x02
## Accel Full Scale Select 16G
AFS_16G  = 0x03

# AK8963 Register Addresses
AK8963_ST1        = 0x02
AK8963_MAGNET_OUT = 0x03
AK8963_CNTL1      = 0x0A
AK8963_CNTL2      = 0x0B
AK8963_ASAX       = 0x10

# CNTL1 Mode select
## Power down mode
AK8963_MODE_DOWN   = 0x00
## One shot data output
AK8963_MODE_ONE    = 0x01

## Continous data output 8Hz
AK8963_MODE_C8HZ   = 0x02
## Continous data output 100Hz
AK8963_MODE_C100HZ = 0x06

# Magneto Scale Select
## 14bit output
AK8963_BIT_14 = 0x00
## 16bit output
AK8963_BIT_16 = 0x01

bus = smbus.SMBus(1)

class MPU9250:

    def __init__(self, address=SLAVE_ADDRESS, accelRangeIn=AFS_16G, gyroRangeIn=GFS_2000):
        self.accelRange = accelRangeIn
        self.gyroRange = gyroRangeIn
        self.address = address
        self.configMPU9250(gyroRangeIn, AFS_2G)
        self.configAK8963(AK8963_MODE_C8HZ, AK8963_BIT_16)

        #Calibration Values
        self.GX_OFFSET = 0
        self.GY_OFFSET = 0
        self.GZ_OFFSET = 0
        self.calibrated = False

        #Integration Values
        timeAtZero = time.time()
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.timeFloat = 0
        self.timeAtStart = 0
        self.timeAtZero = time.time()

        #magnometer calibration offsets
        self.MagXError = 0
        self.MagYError = 0
        self.MagZError = 0



    ##  Makes sure the device is the correct device by reading the value stored in the WHO_AM_I register.
    def searchDevice(self):

        who_am_i = bis.read_byte_data(self.address, WHO_AM_I)

        if(who_am_i == DEVICE_ID):
            return True
        else:
            return False

    ## Configure MPU-9250
    #  @param [in] self The object pointer.
    #  @param [in] gfs Gyro Full Scale Select(default:GFS_250[+250dps])
    #  @param [in] afs Accel Full Scale Select(default:AFS_2G[2g])
    def configMPU9250(self, gfs, afs):
        if gfs == GFS_250:
            self.gres = 250.0/32768.0
        elif gfs == GFS_500:
            self.gres = 500.0/32768.0
        elif gfs == GFS_1000:
            self.gres = 1000.0/32768.0
        else:  # gfs == GFS_2000
            self.gres = 2000.0/32768.0

        if afs == AFS_2G:
            self.ares = 2.0/32768.0
        elif afs == AFS_4G:
            self.ares = 4.0/32768.0
        elif afs == AFS_8G:
            self.ares = 8.0/32768.0
        else: # afs == AFS_16G:
            self.ares = 16.0/32768.0

        # sleep off
        bus.write_byte_data(self.address, PWR_MGMT_1, 0x00)
        time.sleep(0.1)
        # auto select clock source
        bus.write_byte_data(self.address, PWR_MGMT_1, 0x01)
        time.sleep(0.1)
        # DLPF_CFG
        bus.write_byte_data(self.address, CONFIG, 0x03)
        # sample rate divider
        bus.write_byte_data(self.address, SMPLRT_DIV, 0x04)
        # gyro full scale select
        bus.write_byte_data(self.address, GYRO_CONFIG, gfs << 3)
        # accel full scale select
        bus.write_byte_data(self.address, ACCEL_CONFIG, afs << 3)
        # A_DLPFCFG
        bus.write_byte_data(self.address, ACCEL_CONFIG_2, 0x03)
        # BYPASS_EN
        bus.write_byte_data(self.address, INT_PIN_CFG, 0x02)
        time.sleep(0.1)


    ## Configure AK8963
    #  @param [in] self The object pointer.
    #  @param [in] mode Magneto Mode Select(default:AK8963_MODE_C8HZ[Continous 8Hz])
    #  @param [in] mfs Magneto Scale Select(default:AK8963_BIT_16[16bit])
    def configAK8963(self, mode, mfs):
        if mfs == AK8963_BIT_14:
            self.mres = 4912.0/8190.0
        else: #  mfs == AK8963_BIT_16:
            self.mres = 4912.0/32760.0

        bus.write_byte_data(AK8963_SLAVE_ADDRESS, AK8963_CNTL1, 0x00)
        time.sleep(0.01)

        # set read FuseROM mode
        bus.write_byte_data(AK8963_SLAVE_ADDRESS, AK8963_CNTL1, 0x0F)
        time.sleep(0.01)

        # read coef data
        data = bus.read_i2c_block_data(AK8963_SLAVE_ADDRESS, AK8963_ASAX, 3)

        self.magXcoef = (data[0] - 128) / 256.0 + 1.0
        self.magYcoef = (data[1] - 128) / 256.0 + 1.0
        self.magZcoef = (data[2] - 128) / 256.0 + 1.0

        # set power down mode
        bus.write_byte_data(AK8963_SLAVE_ADDRESS, AK8963_CNTL1, 0x00)
        time.sleep(0.01)

        # set scale&continous mode
        bus.write_byte_data(AK8963_SLAVE_ADDRESS, AK8963_CNTL1, (mfs<<4|mode))
        time.sleep(0.01)

    ## brief Check data ready
    #  @param [in] self The object pointer.
    #  @retval true data is ready
    #  @retval false data is not ready
    def checkDataReady(self):
        drdy = bus.read_byte_data(self.address, INT_STATUS)
        if drdy & 0x01:
            return True
        else:
            return False

    ## Read accelerometer
    #  @param [in] self The object pointer.
    #  @retval x : x-axis data
    #  @retval y : y-axis data
    #  @retval z : z-axis data
    def readAccel(self):
        data = bus.read_i2c_block_data(self.address, ACCEL_OUT, 6)
        x = self.dataConv(data[1], data[0])
        y = self.dataConv(data[3], data[2])
        z = self.dataConv(data[5], data[4])

        x = round(x*self.ares, 3)
        y = round(y*self.ares, 3)
        z = round(z*self.ares, 3)

        return {"x":x, "y":y, "z":z}

    ## Read gyro
    #  @param [in] self The object pointer.
    #  @retval x : x-gyro data
    #  @retval y : y-gyro data
    #  @retval z : z-gyro data
    def readGyro(self):
        data = bus.read_i2c_block_data(self.address, GYRO_OUT, 6)

        x = self.dataConv(data[1], data[0])
        y = self.dataConv(data[3], data[2])
        z = self.dataConv(data[5], data[4])

        xPre = round(x*self.gres, 3)
        yPre = round(y*self.gres, 3)
        zPre = round(z*self.gres, 3)

        if self.calibrated:
            x = xPre - self.GX_OFFSET
            y = yPre - self.GY_OFFSET
            z = zPre - self.GZ_OFFSET
        else:
            x = xPre
            y = yPre
            z = zPre

        if self.calibrated:
            timeVar = self.timeElapsed(time.time())
            self.roll += x * timeVar
            self.pitch += y * timeVar
            self.yaw += z * timeVar

        return {"x": round(x, 4), "y": round(y, 4), "z": round(z, 4)}

    ## Read magneto
    #  @param [in] self The object pointer.
    #  @retval x : X-magneto data
    #  @retval y : y-magneto data
    #  @retval z : Z-magneto data
    def readMagnet(self):
        x=0
        y=0
        z=0

        # check data ready
        drdy = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK8963_ST1)
        if drdy & 0x01 :
            data = bus.read_i2c_block_data(AK8963_SLAVE_ADDRESS, AK8963_MAGNET_OUT, 7)

            # check overflow
            if (data[6] & 0x08)!=0x08:
                x = self.dataConv(data[0], data[1])
                y = self.dataConv(data[2], data[3])
                z = self.dataConv(data[4], data[5])

                x = round(x * self.mres * self.magXcoef, 3)
                y = round(y * self.mres * self.magYcoef, 3)
                z = round(z * self.mres * self.magZcoef, 3)

        return {"x":x, "y":y, "z":z}


    ## Data Convert
    # @param [in] self The object pointer.
    # @param [in] data1 LSB
    # @param [in] data2 MSB
    # @retval Value MSB+LSB(int 16bit)
    def dataConv(self, data1, data2):
        value = data1 | (data2 << 8)

        if(value & (1 << 16 - 1)):
            value -= (1<<16)
        return value

    ## Calibrate gyro initial error
    # @param [in] self The object pointer.
    def calGyro(self):
        for x in range(100):
            if x % 10 == 0:
                print('w a i t')
            data = self.readGyro()
            self.GX_OFFSET += data["x"]
            self.GY_OFFSET += data["y"]
            self.GZ_OFFSET += data["z"]
            time.sleep(0.05)
        self.calibrated = True

        self.GX_OFFSET = self.GX_OFFSET / 100
        print('GX OFFSET: ' + str(self.GX_OFFSET))
        self.GY_OFFSET = self.GY_OFFSET / 100
        print('GY OFFSET: ' + str(self.GY_OFFSET))
        self.GZ_OFFSET = self.GZ_OFFSET / 100
        print('GZ OFFSET: ' + str(self.GZ_OFFSET))

        return [self.GX_OFFSET, self.GY_OFFSET, self.GZ_OFFSET]

    ## Calculates time elapsed since entered timeElapsed
    # @param [in] timeStart starting frame for time calculation
    # WARNING: returns in milliseconds. I think?
    def timeElapsed(self, timeNow):
        temp = self.timeFloat
        self.timeFloat = timeNow
        #print ('TIME ELAPSED' + str(timeNow - temp))
        return (timeNow - temp)

    def curHeading(self):
        return {"roll": round(self.roll, 3), "pitch": round(self.pitch, 3), "yaw": round(self.yaw, 3)}

    # FUN PURPOSES
    ## Read temperature
    #  @param [out] temperature temperature(degrees C)
    def readTemperature(self):
        data = bus.read_i2c_block_data(self.address, TEMP_OUT, 2)
        temp = self.dataConv(data[1], data[0])

        temp = round((temp / 333.87 + 21.0), 3)
        return temp

    # Direction (y>0) = 90 - [arcTAN(x/y)]*180/pi
    # Direction (y<0) = 270 - [arcTAN(x/y)]*180/pi
    # Direction (y=0, x<0) = 180.0
    # Direction (y=0, x>0) = 0.0
    def readCompass(self):
        data = self.readMagnet()
        toRet = 0
        if (data['y'] > 0):
            toRet = 90 - (math.atan(data['x']/data['y'])) * 180 / math.radians(180)
        if (data['y'] < 0):
            toRet = 90 - (math.atan(data['x']/data['y'])) * 180 / math.radians(180)
        if (data['y'] == 0 and data['x'] < 0):
            toRet = 180.0
        if (data['y'] == 0 and data['x'] < 0):
            toRet = 0.0
        return toRet

    def calMag(self):
        print("rotate 360 degrees on all axes")
        for x in range(100):
            magData = self.readMagnet()
            self.MagXError += magData["x"]
            self.MagYError += magData["y"]
            self.MagZError += magData["z"]
        self.MagXError = self.MagXError / 100
        self.MagYError = self.MagYError / 100
        self.MagZError = self.MagZError / 100
        print("subtract messured error from raw value")


    #error correction: madgwick or kalman
    def kalman(self, axisString, MagError, GyroError):
        sum = MagError + GyroError
        a = MagError/sum
        b = GyroError/sum
        magComb = self.readMagnet()
        gyroComb = self.readGyro()
        outputGiv = magComb[axisString](a) + gyroComb[axisString](b)
        outputGiv = outputGiv/(a+b)
        print(outputGiv)
