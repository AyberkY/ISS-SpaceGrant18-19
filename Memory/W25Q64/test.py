#Test code for W25Q64FV SPI Flash chipself.
#02/26/2019
import spidev
import time

spi_channel = 0
spi = spidev.SpiDev()
spi.open(0, spi_channel)
print("SPI Channel Initialized.")
spi.max_speed_hz = 500000
spi.mode = 0
time.sleep(1)

print("sending data now...")
time.sleep(0.5)
spi.writebytes([0x90, 0x00, 0x00, 0x00])
data = spi.readbytes(3)
print(data)
