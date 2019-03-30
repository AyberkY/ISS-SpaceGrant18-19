"""
LED Test code!
Pin assignments:
GPIO6 = ORANGE
GPIO13 = GREEN
GPIO19 = BLUE
"""

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)

try:
    while True:
        GPIO.output(6, GPIO.HIGH)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(19, GPIO.LOW)

        time.sleep(0.25)

        GPIO.output(6, GPIO.LOW)
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(19, GPIO.LOW)

        time.sleep(0.25)

        GPIO.output(6, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(19, GPIO.HIGH)

        time.sleep(0.25)

except KeyboardInterrupt:
    GPIO.output(6, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(19, GPIO.LOW)
