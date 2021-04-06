# 8052-python
testing code for ISCG8052. Python scripts that utilise MQTT and SenseHAT.

Instructions:
1. SSH into Pi
2. sudo apt install git python3 sense-hat
3. Reboot (then restart SSH session if it doesn't reconnect)
4. Go to a directory you wish to store the code in (cd folder or mkdir newfolder then cd newfolder)
5. Run git clone https://github.com/scholj05/8052-python.git .
6. cd 8052-python
7. if you haven't yet, install packages using pip (pip install paho-mqtt)
8. nano mqtt-loop.py
9. change broker and topic values on line 8-10
10. CTRL + X (exit file)
11. Y (save changes)
12. ENTER (confirm save)
13. python3 mqtt-loop.py


If you have unwanted local changes, you can overwrite them with the new remote files:
1. git fetch --all
2. git reset --hard origin/main


How to use the code:
Look at the 'mqtt-sample.py' file for the simplest way to use the subscriber and publisher classes.
The Sensors class adds functionality to the SenseHat class (such as temp sensor values adjusted for CPU temp and averaged), but can be used to directly access the SenseHat() object by calling sensors.sense.[attribute/method]
