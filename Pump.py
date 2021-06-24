import RPi.GPIO as GPIO

class Pump:

    def __init__(self, channel):
        self.channel = channel
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.channel, GPIO.OUT)

    def on(self):
        GPIO.output(self.channel, GPIO.HIGH)

    def off(self):
        GPIO.output(self.channel, GPIO.LOW)
