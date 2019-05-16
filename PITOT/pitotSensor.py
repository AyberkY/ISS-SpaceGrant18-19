import smbus, time, math

class PITOT:
    def __init__(self):
        self.slaveAddress = 0x28
        self.bus = smbus.SMBus(1)
        self.offset = 0
        sum = 0
        for i in range(100):
            sum += self.getPressure()
        self.offset = sum / 100

    def getPressure(self):
        data = self.bus.read_i2c_block_data(0x28, 0, 2)
        pressure_raw = data[0] << 8
        pressure_raw += data[1]

        return pressure_raw - self.offset
