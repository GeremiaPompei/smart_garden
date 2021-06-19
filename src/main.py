import RPi.GPIO as GPIO

# GPIO
channelSoil = 21
channelRelay = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(channelSoil, GPIO.IN)
GPIO.setup(channelRelay, GPIO.OUT)

pumpStatus = False

def motor_on(pin):
    GPIO.output(pin, GPIO.HIGH)
    global pumpStatus
    pumpStatus = True

def motor_off(pin):
    GPIO.output(pin, GPIO.LOW)
    global pumpStatus
    pumpStatus = False

def soilStatus():
    return GPIO.input(channelSoil)

def callback(channelSoil, channelRalay):
    if soilStatus():
        motor_on(channelRalay)
    else:
        motor_off(channelRelay)

# thread
import time
import threading

def _autoLoop(stop):
    while True:
        if not stop():
            callback(channelSoil, channelRelay)
        time.sleep(1)

stop_threads = True
autoLoop = threading.Thread(target=_autoLoop, args=(lambda : stop_threads,))
autoLoop.start()

# server
from flask import Flask

app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/pump-on')
def pumpOn():
    motor_on(channelRelay)
    return 'pump on'

@app.route('/auto-on')
def autoOn():
    global stop_threads
    stop_threads = False
    return 'auto on'

@app.route('/pump-off')
def pumpOff():
    global stop_threads
    stop_threads = True
    motor_off(channelRelay)
    return 'pump off'

@app.route('/soil-status')
def soilStatusRoute():
    if soilStatus():
        return 'water not detect'
    else:
        return 'water detect'

@app.route('/pump-status')
def pumpStatusRoute():
    global pumpStatus
    if pumpStatus:
        return 'pump on'
    else:
        return 'pump off'
