import paho.mqtt as mqtt
import paho.mqtt.publish as publish

class Publisher:

    def __init__(self, url, port, topic="unitec/iot/testing", qos=1):
        self.url = url
        self.port = port
        self.topic = topic
        self.qos = qos
        self.client = mqtt.client.Client()
        publish._on_publish = self.on_message
        self.client.connect(self.url, self.port)
        self.client.loop_start()

    def publish(self, message):
        self.client.publish(self.topic, message, self.qos)

    def on_message(self, client, userdata, mid):
        print(f"published {userdata} to {self.topic}")
