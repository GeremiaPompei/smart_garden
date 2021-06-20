import paho.mqtt.client as mqtt

class Publisher:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def publish(self, topic, to_publish):
        self.client = mqtt.Client()
        self.client.connect(self.ip, self.port, 60)
        self.client.publish(topic, to_publish);
        self.client.disconnect()
