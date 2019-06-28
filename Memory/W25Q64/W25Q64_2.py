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
        return self.spi.xfer2([RUID]) #skip 4 first bytes (dummies)

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

#SPI Connection
chip = spiflash(bus = 0, cs = 0)

#Clear Data
chip.erase_all()

#Block ranges for each type of data
rangeTime = 0
rangeAltB = 32
rangeAccl = 64
rangePito = 96
rangeSect = 0 #Sector range
rangePage = 0 #Page range
rangeLine = 0

#Pages of data
dataTime = []
dataAltB = []
dataAccl = []
dataPito = []

#Writing data onto SPI
def writeData(dataArr):

    #Data Array
    dataTime += [hex(dataArr[1]), hex(dataArr[2]), hex(dataArr[3] // 1000), hex(dataArr[3] // 10000 - dataArr[3] // 100)] + [255 for _ in range(8)]
    dataAltB += []
    dataAccl += []
    dataPito += ((5 - len(str(dataArr[14]))) * [0x00]) + [hex(int(str(dataArr[14])[i])) for i in range(len(str(dataArr[14])))] + [255 for _ in range(11)]

    #Write a page
    if not (rangeLine < 16):
        rangeLine = 0

        chip.write(hex(rangeTime), hex(rangeSect), hex(rangePage), dataTime)
        chip.write(hex(rangeAltB), hex(rangeSect), hex(rangePage), dataTime)
        chip.write(hex(rangeAccl), hex(rangeSect), hex(rangePage), dataTime)
        chip.write(hex(rangePito), hex(rangeSect), hex(rangePage), dataTime)

        #Next block
        if not (rangeSect < 16):
            rangeSect = 0
            rangeTime += 1
            rangeAltB += 1
            rangeAccl += 1
            rangePito += 1

    rangeLine += 1
