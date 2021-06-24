import RPi.GPIO as GPIO# GPIO

class Soil:

    def __init__(self, channel):
        self.channel = channel
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.channel, GPIO.IN)

    def status(self):
        return GPIO.input(self.channel)
