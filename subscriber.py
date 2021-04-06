import paho.mqtt as mqtt
import paho.mqtt.subscribe as subscribe

class Subscriber:

    def __init__(self, url, port, topic="unitec/iot/testing", qos=1):
        self.url = url
        self.port = port
        self.topic = topic
        self.qos = qos
        self.client = mqtt.client.Client()

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        subscribe._on_message_callback = self.on_message
        subscribe._on_message_simple = self.on_message
        self.client.connect(self.url, self.port)
        self.client.subscribe(self.topic, self.qos)

    def start(self):
        #self.client.subscribe(self.topic, self.qos)
        self.client.loop_start()

    def stop(self):
        #self.client.unsubscribe(self.topic)
        self.client.loop_stop()

    def on_message(self, client, userdata, message):
        print(f"{message.topic}: {message.payload}")

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {str(rc)}")
