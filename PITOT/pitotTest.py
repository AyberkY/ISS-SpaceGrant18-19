import pitotSensor, time

pitot1 = pitotSensor.PITOT()

while True:
    print(str(pitot1.getPressure()))
    time.sleep(0.1)
