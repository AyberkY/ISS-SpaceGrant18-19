'''
RFM9X Class for SpaceGrant18
'''

import adafruit_rfm9x
import board
import busio
import digitalio
import time

class RFM9X:
    def __init__(self):
        self.RADIO_FREQ_MHZ = 433.0

        self.CS = digitalio.DigitalInOut(board.CE1)
        self.RESET = digitalio.DigitalInOut(board.D25)

        self.spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

        self.rfm9x = adafruit_rfm9x.RFM9x(self.spi, self.CS, self.RESET, self.RADIO_FREQ_MHZ)
        self.rfm9x.tx_power = 23

    def send(self, data):
        self.rfm9x.send(data)

    def receive(self, timeout=0.5, keep_listening=True):
        packet = self.rfm9x.receive(timeout, keep_listening)

        if packet is None:
            return [[], 0]
        else:
            data = str(packet)
            rssi = self.rfm9x.rssi
            return [data, rssi]
