import smbus, time, math

bus = smbus.SMBus(1)

class PITOT:
    def __init__(self):
        self.address = 0x28
        self.offset = 0

    def getPressure(self):
        data = bus.read_i2c_block_data(self.address, 0, 2)
        pressure_raw = data[0] << 8
        pressure_raw += data[1]

        return pressure_raw - self.offset

    def calPressure(self):
        sum = 0
        for i in range(100):
            sum += self.getPressure() - 8192
            time.sleep(0.01)

        self.offset = sum / 100
