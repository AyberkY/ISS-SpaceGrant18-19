import spidev

spi = spidev.SpiDev()
spi.open(0, 0)

#Raspi 3 Pinout Configuration
CLK = 23
MISO = 21
MOSI = 19
CS = 24

#SPI Module Function Dictionaries
moduleFunctions = {}
