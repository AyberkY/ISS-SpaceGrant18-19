import smbus, time, math

class PITOT:
    def __init__(self):
        self.slaveAddress = 0x28
        self.bus = smbus.SMBus(1)

    def getPressure(self):
        data = self.bus.read_i2c_block_data(self.slaveAddress, 0, 2)
        pressure_raw = data[0] << 8
        pressure_raw += data[1]

        return pressure_raw
