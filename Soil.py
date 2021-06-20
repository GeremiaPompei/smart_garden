import RPi.GPIO as GPIO# GPIO

channel = 21

class Soil:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel, GPIO.IN)

    def status(self):
        return GPIO.input(channel)
