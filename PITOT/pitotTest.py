import pitotSensor, time

pitot1 = pitotSensor.PITOT()

#pitot1.calibrate()

print("OFFSET: " + str(pitot1.offset))

time.sleep(1)

while True:
    print(str(pitot1.getPressure()))
    time.sleep(0.1)
