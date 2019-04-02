'''
RFM9X Class for SpaceGrant18
'''

import adafruit_rfm9x
import board
import busio
import digitalio
import time

class RFM9X:
    def __init__():
        self.RADIO_FREQ_MHZ = 433.0
        
        self.CS = digitalio.DigitalInOut(board.CE1)
        self.RESET = digitalio.DigitalInOut(board.D25)

        self.spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

        self.rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
        rfm9x.tx_power = 23

    def send(data):
        self.rfm9x.send(data)

    def receive(timeout=0.5, keep_listening=True):
        data = self.rfm9x.receive(timeout, keep_listening)
        if type(data) != None:
            return data
