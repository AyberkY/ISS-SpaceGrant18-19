# Test code for W25Q64FV SPI Flash chipself.
# 02/26/2019
# 172.16.108.161
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
spi.xfer([0x9F])
data = spi.xfer([0x00])
print(data)
