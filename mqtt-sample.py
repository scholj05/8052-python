# Sample code for how to use the subscriber and publisher files
# in your own projects. Just import, initialise, and use.

# Remove the quotes on line 5 and 19 to use this code.
"""

# import files
import subscriber
import publisher

# initialise objects
sub = subscriber.Subscriber("broker.hivemq.com", 1883, "unitec/iot/testing", 1)
pub	= publisher.Publisher("broker.hivemq.com", 1883, "unitec/iot/testing", 1)

# use them in code
if __name__ == '__main__':
    sub.start()
    pub.publish("hello")
"""