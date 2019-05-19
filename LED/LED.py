"""
Pin assignments:
GPIO6 = ORANGE
GPIO13 = GREEN
GPIO19 = BLUE
GPIO20 = BUZZER
"""

import RPi.GPIO as GPIO
import time

class LED:
    def __init__(self, color):
        GPIO.setmode(GPIO.BCM)

        if color == 'orange':
            self.pinNumber = 6
        elif color == 'green':
            self.pinNumber = 13
        elif color == 'blue':
            self.pinNumber = 19

        GPIO.setup(self.pinNumber, GPIO.OUT)

    def setHigh(self):
        GPIO.output(self.pinNumber, GPIO.HIGH)

    def setLow(self):
        GPIO.output(self.pinNumber, GPIO.LOW)

class BUZZER:
    def __init__(self, enabled=True):
        GPIO.setmode(GPIO.BCM)
        self.pinNumber = 20
        GPIO.setup(self.pinNumber, GPIO.OUT)
        self.enabled = enabled

    def setHigh(self):
        if self.enabled:
            GPIO.output(self.pinNumber, GPIO.HIGH)

    def setLow(self):
        GPIO.output(self.pinNumber, GPIO.LOW)
