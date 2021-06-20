import RPi.GPIO as GPIO
import time
import threading
import paho.mqtt.client as mqtt

# Object
class MQTTClientSubscriber:

    def __init__(self, ip, port, topic, on_message):
        self.topic = topic
        client = mqtt.Client()
        client.connect(ip,port,60)
        client.on_connect = self.on_connect
        client.on_message = on_message
        client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe(self.topic)


class MQTTClientPublisher:

    def __init__(self, ip, port, topic, to_publish):
        client = mqtt.Client()
        client.connect(ip, port, 60)
        client.publish(topic, to_publish);
        client.disconnect()

# GPIO
channelSoil = 21
channelRelay = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(channelSoil, GPIO.IN)
GPIO.setup(channelRelay, GPIO.OUT)

def motor_on(pin):
    GPIO.output(pin, GPIO.HIGH)

def motor_off(pin):
    GPIO.output(pin, GPIO.LOW)


def soilStatus():
    return GPIO.input(channelSoil)

def callback(channelSoil, channelRalay, stop):
    if soilStatus():
        if not stop():
            motor_on(channelRalay)
            MQTTClientPublisher('localhost', 1883, 'handle/pump', 'ON')
        MQTTClientPublisher('localhost', 1883, 'status/soil', 'Water Not Detected')
    else:
        if not stop():
            motor_off(channelRelay)
            MQTTClientPublisher('localhost', 1883, 'handle/pump', 'OFF')
        MQTTClientPublisher('localhost', 1883, 'status/soil', 'Water Detected')


# thread
def _autoLoop(stop):
    while True:
        callback(channelSoil, channelRelay, stop)
        time.sleep(1)

stop_threads = True
autoLoop = threading.Thread(target=_autoLoop, args=(lambda : stop_threads,))
autoLoop.start()

# server
def on_message_handle_pump_auto(client, userdata, msg):
    global stop_threads
    if msg.payload.decode() == "ON":
        stop_threads = False
    else:
        stop_threads = True

def on_message_handle_pump_manual(client, userdata, msg):
    global channelRelay
    if msg.payload.decode() == "ON":
        motor_on(channelRelay)
    else:
        motor_off(channelRelay)

def on_message_soil_status(client, userdata, msg):
    return soilStatus()

MQTTClientSubscriber('localhost', 1883, 'handle/pump', on_message_handle_pump_manual)
MQTTClientSubscriber('localhost', 1883, 'handle/auto', on_message_handle_pump_auto)
