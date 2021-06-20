import time
import threading

from Subscriber import Subscriber
from Publisher import Publisher
from Soil import Soil
from Pump import Pump

# mqtt connection data
mqtt_ip = "localhost"
mqtt_port = 1883

# topics
TOPIC_HANDLE_PUMP = 'handle/pump'
TOPIC_HANDLE_AUTO = 'handle/auto'
TOPIC_STATUS_SOIL = 'status/soil'

# global variable to start and stop auto
stop_thread = True

subscriber = Subscriber(mqtt_ip, mqtt_port)
publisher = Publisher(mqtt_ip, mqtt_port)

soil = Soil()
pump = Pump()

# threading functions
def publish_pump(status):
    global status_thread
    if not stop_thread:
        publisher.publish(TOPIC_HANDLE_PUMP, status)

def callback():
    if soil.status():
        publish_pump('ON')
        publisher.publish(TOPIC_STATUS_SOIL, 'Water Not Detected')
    else:
        publish_pump('OFF')
        publisher.publish(TOPIC_STATUS_SOIL, 'Water Detected')

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
    subscriber.subscribe(TOPIC_HANDLE_AUTO, on_message_auto)
    subscriber.subscribe(TOPIC_HANDLE_PUMP, on_message_pump)
