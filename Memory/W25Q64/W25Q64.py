WREN  = 0x06
WRDI  = 0x04
RDSR1 = 0x05
RDSR2 = 0x35
WRSR  = 0x01
READ  = 0x03
WRITE = 0x02
RUID  = 0x4B
SECTOR_ERASE = 0x20
CHIP_ERASE = 0xC7

from time import sleep
import spidev
from datetime import datetime

def sleep_ms(msecs):
    sleep(float(msecs) / 1000.0)

class spiflash(object):

    def __init__(self, bus, cs, mode = 0, max_speed_hz = 1000000):
        self.spi = spidev.SpiDev()
        self.spi.open(bus,cs)
        self.spi.max_speed_hz = max_speed_hz
        self.spi.mode = mode

    def __del__(self):
        try:
            self.spi.close()
        except:
            pass

    #reads ----------------------------------------------------------------------------------
    def read_status(self):
        statreg = self.spi.xfer2([RDSR1,RDSR1])[1]
        statreg2 = self.spi.xfer2([RDSR2,RDSR2])[1]
        return statreg, statreg2

    def read_page(self, adr1, adr2):
        xfer = [READ, adr1, adr2, 0] + [255 for _ in range(256)] # command + 256 dummies
        return self.spi.xfer2(xfer)[4:] #skip 4 first bytes (dummies)

    #writes ----------------------------------------------------------------------------------
    def write_enable(self):
        self.spi.xfer2([WREN])
        sleep_ms(5)

    def write_disable(self):
        self.spi.xfer2([WRDI])
        sleep_ms(5)

    def write_status(self,s1,s2):
        self.write_enable()

        spi.xfer2([WRSR,s1,s2])
        sleep_ms(10)

        self.wait_until_not_busy()

    def write_page(self, addr1, addr2, page):
        self.write_enable()

        xfer = [WRITE, addr1, addr2, 0] + page[:256]
        self.spi.xfer2(xfer)
        sleep_ms(10)

        self.wait_until_not_busy()

    def write_and_verify_page(self, addr1, addr2, page):
        self.write_page(addr1, addr2, page)
        return self.read_page(addr1, addr2)[:256] == page[:256]

    #erases ----------------------------------------------------------------------------------
    def erase_sector(self,addr1, addr2):
        self.write_enable()

        xfer = [SECTOR_ERASE, addr1, addr2, 0]
        self.spi.xfer2(xfer)
        sleep_ms(10)

        self.wait_until_not_busy()

    def erase_all(self):
        self.write_enable()

        self.spi.xfer2([CHIP_ERASE])
        sleep_ms(10)

        self.wait_until_not_busy()

    #misc ----------------------------------------------------------------------------------
    def wait_until_not_busy(self):
        statreg = 0x1;
        while (statreg & 0x1) == 0x1:
            #Wait for the chip.
            statreg = self.spi.xfer2([RDSR1, RDSR1])[1]
            #print "%r \tRead %X" % (datetime.now(), statreg)
            sleep_ms(5)

    def read_UID(self): #added
        return self.spi.xfer2([RUID]) #skip 4 first bytes ()

    #helpers -------------------------------------------------------------------------------
    def print_status(self,status):
        print("status " + bin(status[1])[2:].zfill(8) + " " + bin(status[0])[2:].zfill(8))

    def print_page(self, page):
        s = ""
        for row in range(16):
            for col in range(16):
                s += hex(page[row * 16 + col])[2:] + " "
            s += "\n"
        print(s)


#Initializaiton -------------------------------------------------------------------------------

#Formatting functions (Makes data entry easier)
def decToHex(num):
    data = ""
    for i in str(num):
        if i == ".":
            data += "F"
        else:
            data += i
    return data

def dataFormat(data):
    newData = []
    data = decToHex(data)
    for i in range(8):
        if (len(data) - (len(newData)*2)) >= 2:
            newData += [hex(int(data[i*2: (i+1)*2], 16))]
        else:
            newData += [0xFF]
    return newData

def dataFormat_int(data):
    data = decToHex(data)
    temp = ""
    for i in range(len(data)):
        temp += data[i]
        if (i == (len(data) - 1)):
            temp += "F"
    return dataFormat(temp)

#Reading the entire chip
def readSPI():
    data = []
    for i in range(128):
        for j in range(256):
            data.append(chip.read_page(i, j))
    return data

def csvSPI(data):
    
    return csvData

#SPI Connection
chip = spiflash(bus = 0, cs = 0)

#Clear Data
chip.erase_all()

#Block ranges for each type of data
rangeTime  = 0   #Time
rangeLat   = 8   #Latitude
rangeLot   = 16  #Longitude
rangeAlt   = 24  #Altitude
rangeSat   = 32  #Satellites
rangeBPres = 40  #Barometric Pressure
rangeBAlt  = 48  #BArometric Altitude
rangeCTemp = 56  #Temperature in Celsius
rangePPres = 64  #Pitot Tube Pressure
rangeAcclX = 72  #Acceleration X
rangeAcclY = 80  #Acceleration Y
rangeAcclZ = 88  #Acceleration Z
rangeGyroX = 96  #Gyroscope X
rangeGyroY = 104 #Gyroscope Y
rangeGyroZ = 112 #Gyroscope Z

rangeSect = 0 #Sector range
rangePage = 0 #Page range
rangeLine = 0 #Line range

#Pages of data
dataTime  = []
dataLat   = []
dataLot   = []
dataAlt   = []
dataSat   = []
dataBPres = []
dataBAlt  = []
dataCTemp = []
dataPPres = []
dataAcclX = []
dataAcclY = []
dataAcclZ = []
dataGyroX = []
dataGyroY = []
dataGyroZ = []

#Loop Function -----------------------------------------------------------------

#Writing data onto SPI page by page
def writeData(dataArr):

    #Data Array
    dataTime.append([dataFormat(dataArr[0])])
    dataLat.append(dataFormat(dataArr[2]))
    dataLot.append(dataFormat(dataArr[3]))
    dataAlt.append(dataFormat(dataArr[4])])
    dataSat.append(dataFormat_int(dataArr[5])])
    dataBPres.append(dataFormat(dataArr[9])])
    dataBAlt.append(dataFormat(dataArr[10])])
    dataCTemp.append(dataFormat(dataArr[11])])
    dataPPres.append(dataFormat(dataArr[12])])
    dataAcclX.append(dataFormat(dataArr[13])])
    dataAcclY.append(dataFormat(dataArr[14])])
    dataAcclZ.append(dataFormat(dataArr[15])])
    dataGyroX.append(dataFormat(dataArr[16])])
    dataGyroY.append(dataFormat(dataArr[17])])
    dataGyroZ.append(dataFormat(dataArr[18])])

    #Write a page
    if not (rangeLine < 16):
        rangeLine = 0

        chip.write(hex(rangeTime ), hex(rangeSect), hex(rangePage), dataTime )
        chip.write(hex(rangeLat  ), hex(rangeSect), hex(rangePage), dataLat  )
        chip.write(hex(rangeLot  ), hex(rangeSect), hex(rangePage), dataLot  )
        chip.write(hex(rangeAlt  ), hex(rangeSect), hex(rangePage), dataAlt  )
        chip.write(hex(rangeSat  ), hex(rangeSect), hex(rangePage), dataSat  )
        chip.write(hex(rangeBPres), hex(rangeSect), hex(rangePage), dataBPres)
        chip.write(hex(rangeBAlt ), hex(rangeSect), hex(rangePage), dataBAlt )
        chip.write(hex(rangeCTemp), hex(rangeSect), hex(rangePage), dataCTemp)
        chip.write(hex(rangePPres), hex(rangeSect), hex(rangePage), dataPPres)
        chip.write(hex(rangeAcclX), hex(rangeSect), hex(rangePage), dataAcclX)
        chip.write(hex(rangeAcclY), hex(rangeSect), hex(rangePage), dataAcclY)
        chip.write(hex(rangeAcclZ), hex(rangeSect), hex(rangePage), dataAcclZ)
        chip.write(hex(rangeGyroX), hex(rangeSect), hex(rangePage), dataGyroX)
        chip.write(hex(rangeGyroY), hex(rangeSect), hex(rangePage), dataGyroY)
        chip.write(hex(rangeGyroZ), hex(rangeSect), hex(rangePage), dataGyroZ)

        #Reset the data
        dataTime  = []
        dataLat   = []
        dataLot   = []
        dataAlt   = []
        dataSat   = []
        dataBPres = []
        dataBAlt  = []
        dataCTemp = []
        dataPPres = []
        dataAcclX = []
        dataAcclY = []
        dataAcclZ = []
        dataGyroX = []
        dataGyroY = []
        dataGyroZ = []

        #Next block
        if not (rangeSect < 16):
            rangeSect = 0
            rangeTime  += 1  #Time
            rangeLat   += 1  #Latitude
            rangeLot   += 1  #Longitude
            rangeAlt   += 1  #Altitude
            rangeSat   += 1  #Satellites
            rangeBPres += 1  #Barometric Pressure
            rangeBAlt  += 1  #BArometric Altitude
            rangeCTemp += 1  #Temperature in Celsius
            rangePPres += 1  #Pitot Tube Pressure
            rangeAcclX += 1  #Acceleration X
            rangeAcclY += 1  #Acceleration Y
            rangeAcclZ += 1  #Acceleration Z
            rangeGyroX += 1  #Gyroscope X
            rangeGyroY += 1  #Gyroscope Y
            rangeGyroZ += 1  #Gyroscope Z

    rangeLine += 1
