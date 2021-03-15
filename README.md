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
