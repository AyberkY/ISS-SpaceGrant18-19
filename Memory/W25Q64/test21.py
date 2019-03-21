WREN  = 0x06
WRDI  = 0x04
RDSR1 = 0x05
RDSR2 = 0x35
WRSR  = 0x01
READ  = 0x03
WRITE = 0x02
SECTOR_ERASE = 0x20
CHIP_ERASE = 0xC7

from time import sleep
import spidev
from datetime import datetime
import binascii

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
        statreg = self.spi.xfer2([RDSR,RDSR])[1]
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

    #helpers -------------------------------------------------------------------------------
    def print_status(self,status):
        print "status %s %s" % (bin(status[1])[2:].zfill(8), bin(status[0])[2:].zfill(8))

    def print_page(self, page):
        s = ""
        for row in range(16):
            for col in range(15):
                s += "%02X " % page[row * 16 + col]
            s += "\n"
        print s


#TESTS -------------------------------------------------------------------
#TESTS -------------------------------------------------------------------

chip = spiflash(bus = 0, cs = 0)

#Reading UI
try:
    while True:
        block  = hex(input("Block (0-127): "))
        sector = hex(input("Sector (0-16): "))
        pageN   = hex(input("Page   (0-16): "))

        page = chip.read_page(int(block, 16), int((sector[2:]+pageN[2:]), 16))
        chip.print_page(page)
except KeyboardInterrupt:
    print('interrupted!')


#Writing Strings UI

string = input('String: ')
pageBe = chip.read_page(0x00, 0x00)

page = []
for i in range(256):
    try:
        page.append(int('0x' + binascii.hexlify(str.encode(string[i])).decode("utf-8"), 0))
    except:
        page.append(0x00)

print(page)
print(len(page))

print(chip.write_and_verify_page(0x00, 0x00, page))
pageAf = chip.read_page(0x00, 0x00)

chip.print_page(pageBe)
chip.print_page(pageAf)
