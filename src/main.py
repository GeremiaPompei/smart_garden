import time
import threading

from MQTTClient import MQTTClient
from Soil import Soil
from Pump import Pump

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# mqtt connection data
MQTT_IP = os.environ.get("MQTT_IP")
MQTT_PORT = (int)(os.environ.get("MQTT_PORT"))

# topics
TOPIC_HANDLE_PUMP = os.environ.get("TOPIC_HANDLE_PUMP")
TOPIC_HANDLE_AUTO = os.environ.get("TOPIC_HANDLE_AUTO")
TOPIC_STATUS_SOIL = os.environ.get("TOPIC_STATUS_SOIL")

# pins
PIN_PUMP = (int)(os.environ.get("PIN_PUMP"))
PIN_SOIL = (int)(os.environ.get("PIN_SOIL"))

# global variable to start and stop auto
stop_thread = True

mqtt_client = MQTTClient(MQTT_IP, MQTT_PORT)

soil = Soil(PIN_SOIL)
pump = Pump(PIN_PUMP)

# threading functions
def publish_pump(status):
    global status_thread
    if not stop_thread:
        mqtt_client.publish(TOPIC_HANDLE_PUMP, status)

def callback():
    if soil.status():
        publish_pump('ON')
        mqtt_client.publish(TOPIC_STATUS_SOIL, 'Water Not Detected')
    else:
        publish_pump('OFF')
        mqtt_client.publish(TOPIC_STATUS_SOIL, 'Water Detected')

def loop():
    while True:
        callback()
        time.sleep(1)

# on_message functions
def on_message_auto(client, userdata, msg):
    global stop_thread
    stop_thread = msg.payload.decode() != "ON"

def on_message_pump(client, userdata, msg):
    global pump
    if msg.payload.decode() == "ON":
        pump.on()
    else:
        pump.off()

# main function
if __name__ == "__main__":
    thread = threading.Thread(target=loop)
    thread.start()
    mqtt_client.subscribe(TOPIC_HANDLE_AUTO, on_message_auto)
    mqtt_client.subscribe(TOPIC_HANDLE_PUMP, on_message_pump)
