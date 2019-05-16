import pitotSensor, time

pitot1 = pitotSensor.PITOT()

pitot1.calibrate()

print("OFFSET: " + pitot1.offsets)

time.sleep(1)

while True:
    print(str(pitot1.getPressure()))
    time.sleep(0.1)
