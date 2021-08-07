import paho.mqtt.client as mqtt

class MQTTClient:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def publish(self, topic, to_publish):
        self.client = mqtt.Client()
        self.client.connect(self.ip, self.port, 60)
        self.client.publish(topic, to_publish, 0, True);
        self.client.disconnect()

    def subscribe(self, topic, on_message):
        client = mqtt.Client()
        client.connect(self.ip, self.port, 60)
        client.on_connect = lambda client, userdata, flags, rc : self.on_connect(client, userdata, flags, rc, topic)
        client.on_message = on_message
        client.loop_start()
        return client

    def on_connect(self, client, userdata, flags, rc, topic):
        print("[" + topic + "]: connected with result code " + str(rc))
        client.subscribe(topic)
