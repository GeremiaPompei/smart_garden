import RPi.GPIO as GPIO

channel = 16

class Pump:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel, GPIO.OUT)

    def on(self):
        GPIO.output(channel, GPIO.HIGH)

    def off(self):
        GPIO.output(channel, GPIO.LOW)
