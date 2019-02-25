# Dedicated to my beloved Professor
# May he rest gayly
#02/22/2019

import smbus
import time
import math

## MPU9250 Default I2C slave address
SLAVE_ADDRESS        = 0x68
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

## smbus
bus = smbus.SMBus(1)
timeFloat = 0
timeAtZero = 0

class MPU9250:



    def __init__(self, address=SLAVE_ADDRESS, accelRangeIn=AFS_16G, gyroRangeIn=GFS_2000):
        self.accelRange = accelRangeIn
        self.gyroRange = gyroRangeIn
        self.address = address
        self.configMPU9250(GFS_250, AFS_2G)
        self.GX_OFFSET = 0
        self.GY_OFFSET = 0
        self.GZ_OFFSET = 0
        self.calibrated = False
        mpu9250.timeAtZero = time.time()
        self.roll = 0
        self.pitch = 0
        self.yaw = 0



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

        return {"x":x, "y":y, "z":z, "xPre":xPre, "yPre":yPre, "zPre":zPre}

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
                print('PLEASE WAIT. YOUR DATA IS IMPORTANT TO US')
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

    ## Calculates time elapsed since entered timeElapsed
    # @param [in] timeStart starting frame for time calculation
    # WARNING: returns in milliseconds. I think?
    def timeElapsed(self, timeStart):
        timeFloat = time.time()
        return (timeFloat - timeStart - timeAtZero)


    def curHeading(self):
        data = self.readGyro()
