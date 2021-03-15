import paho.mqtt.client as mqtt
from sense_hat import SenseHat
import time
from threading import Timer


client 		= mqtt.Client()
BROKER_URL 	= "broker.hivemq.com"
BROKER_PORT 	= 1883
TOPIC 		= "unitec/iot/jesse" 
SHOULD_REPORT 	= True
POLL_RATE	= 10.0
sense 		= SenseHat()
last_poll_time = 0.0
W = [	150, 	150, 	150	]
R = [	150, 	0, 	0	]
G = [	0, 	150, 	0	]
B = [	0, 	0, 	150	]
E = [	0, 	0, 	0	]



def init():
	print("init started...")
	client.on_subscribe = on_subscribe
	client.on_message = on_message
	client.connect(BROKER_URL, BROKER_PORT)
	client.subscribe(TOPIC, qos=1)
	last_poll_time = time.time()
	print("init complete.")


def on_subscribe(client, userdata, mid, granted_qos):
	print("Subscribed to " + str(mid) + " with QoS " + str(granted_qos))


def on_message(client, userdata, msg):
	print(msg.topic + ": " + str(msg.payload))
	Timer(0, blink(1, 1, B, 1))


def blink(x, y, colour, blinkCount, delay):
	for i in range(0, blinkCount):
		sense.set_pixel(x, y, colour)
		time.sleep(delay)
		sense.set_pixel(x, y, E)
		time.sleep(delay)


def get_sensor_data():
	return [sense.get_temperature(),
		sense.get_pressure(),
		sense.get_humidity()
	]


def read_report():
	if SHOULD_REPORT:
		snsr_data = get_sensor_data()
		msg = f"[ temperature: {snsr_data[0]},\npressure: {snsr_data[1]}\nhumidity: {snsr_data[2]}]" 
		client.publish(TOPIC, msg, qos=1)


if __name__ == '__main__':
	init()
	while True:
		for event in sense.stick.get_events():
			if event.action == "pressed":
				SHOULD_REPORT = not SHOULD_REPORT
				print(f"publishing status: {SHOULD_REPORT}")
		
		time_now = time.time()
		
		if time_now - last_poll_time > POLL_RATE:
			read_report()
			last_poll_time = time_now


