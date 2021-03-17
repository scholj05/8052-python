import paho.mqtt.client as mqtt
from sense_hat import SenseHat
from threading import Timer
from datetime import datetime, timedelta
import time


client 		= mqtt.Client()
BROKER_URL 	= "broker.hivemq.com"
BROKER_PORT 	= 1883
TOPIC 		= "unitec/iot/jesse" 
SHOULD_REPORT 	= True
POLL_RATE	= 10.0
sense 		= SenseHat()
last_poll_time = datetime.now() - timedelta(seconds=10)

W = [	150, 	150, 	150	]
R = [	150, 	0, 	0	]
G = [	0, 	150, 	0	]
B = [	0, 	0, 	150	]
E = [	0, 	0, 	0	]

# callback methods. Only work if using the mqtt.run() method
def on_connect(client, userdata, flags, rc):
	print("Connected to " + BROKER + "with result: " + str(rc))


def on_subscribe(client, userdata, mid, granted_qos):
	print("Subscribed to " + str(mid) + " with QoS " + str(granted_qos))


def on_message(client, userdata, msg):
	print(msg.topic + ": " + str(msg.payload))
	Timer(0, blink(1, 1, B, 1))

# method for using the LEDs. Should probably be used in separate thread
def blink(x, y, colour, blinkCount, delay):
	for i in range(0, blinkCount):
		sense.set_pixel(x, y, colour)
		time.sleep(delay)
		sense.set_pixel(x, y, E)
		time.sleep(delay)

# method to fetch current sensor values
def get_sensor_data():
	return [sense.get_temperature(),
		sense.get_pressure(),
		sense.get_humidity()
	]

# get sensor data and send as mqtt publish payload
def read_report():
	if SHOULD_REPORT:
		snsr_data = get_sensor_data()
		timeNow = datetime.now()
		msg = f"[\n\ttemperature: {snsr_data[0]},\n" \
			f"\tpressure: {snsr_data[1]},\n" \
			f"\thumidity: {snsr_data[2]}\n" \
			f"] captured at {timeNow}" 
		client.publish(TOPIC, msg, qos=1)
		print(f"Attempted to publish data at {timeNow}")
		blink(0, 0, W, 2, 0.25)

# setup the client
def init():
	print("init started...")
	client.on_connect = on_connect
	client.on_subscribe = on_subscribe
	client.on_message = on_message
	client.connect(BROKER_URL, BROKER_PORT)
	client.subscribe(TOPIC, qos=1)
	#last_poll_time = time.time()
	print("init complete.")


# main method. Starting point of program.
if __name__ == '__main__':
	init()
	while True:
		for event in sense.stick.get_events():
			if event.action == "pressed":
				last_poll_time -= timedelta(seconds=10)
				SHOULD_REPORT = not SHOULD_REPORT
				print(f"publishing status: {SHOULD_REPORT}")
		
		time_now = datetime.now()
		if float((time_now - last_poll_time).total_seconds()) > POLL_RATE:
			read_report()
			last_poll_time = time_now


