import paho.mqtt.client as mqtt
from sense_hat import SenseHat
from threading import Timer
from datetime import datetime, timedelta
import time
import subscriber
import publisher
import sensors


BROKER_URL 		= "broker.hivemq.com"
BROKER_PORT 	= 1883
TOPIC 			= "unitec/iot/jesse" 
SHOULD_REPORT 	= True
POLL_RATE		= 10.0

sub 			= subscriber.Subscriber(BROKER_URL, BROKER_PORT, TOPIC, 1)
pub				= publisher.Publisher(BROKER_URL, BROKER_PORT, TOPIC, 1)
sense 			= sensors.Sensors()
last_poll_time 	= datetime.now() - timedelta(seconds=10)

W = [	150, 	150, 	150	]
R = [	150, 	0, 		0	]
G = [	0, 		150, 	0	]
B = [	0, 		0, 		150 ]
E = [	0, 		0, 		0	]


# method for using the LEDs. Should probably be used in separate thread
def blink(x, y, colour, blinkCount, delay):
	for i in range(0, blinkCount):
		sense.fill(colour[0], colour[1], colour[2])
		time.sleep(delay)
		sense.clear()
		time.sleep(delay)

# method to fetch current sensor values
def get_sensor_data():
	return sense.get_enviro_data()

# get sensor data and send as mqtt publish payload
def read_report():
	if SHOULD_REPORT:
		t, p, h = sense.get_enviro_data()
		timeNow = datetime.now()
		msg = f"[\n\ttemperature: {round(t, 1)},\n" \
			f"\tpressure: {round(p)},\n" \
			f"\thumidity: {round(h)}\n" \
			f"] captured at {timeNow}" 
		pub.publish(msg)
		print(f"Attempted to publish data at {timeNow}")
		blink(0, 0, G, 2, 0.25)

# setup the client
def init():
	print("init started...")
	sub.start()


# main method. Starting point of program.
if __name__ == '__main__':
	init()
	while True:
		for event in sense.sense.stick.get_events():
			if event.action == "pressed":


				last_poll_time -= timedelta(seconds=10)
				SHOULD_REPORT = not SHOULD_REPORT
				print(f"publishing status: {SHOULD_REPORT}")
		
		time_now = datetime.now()
		if float((time_now - last_poll_time).total_seconds()) > POLL_RATE:
			read_report()
			last_poll_time = time_now


