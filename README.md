# SIT210_Project
This folder contains source code for my project for SIT210 - Embedded Systems Development project.
This prototype is for an obstace detection system on a remote controlled car.
The on board system contains a Sharp IR sensor and Particle Argon.
The central system is a raspberry pi with a GUI, 4 relay bank and buzzer
Communication between the two is through MQTT.

Hardware Requires:
•	Particle Argon
•	Miniature breadboard
•	Sharp IR distance sensor
•	3.3V to 5V converter
•	Battery pack
•	Jumper cables
•	Remote controlled car
•	Raspberry Pi 
•	Micro SD card
•	Power supply
•	4-channel relay bank
•	Breadboard
•	Buzzer
•	Remote controlled car controller

Software Required:
•	Particle Web IDE
•	NOOBS operating system (installed on micro SD card)
•	Python IDE

On-Board System:
Ensure the IR distance sensor is mounted securely to the front of the vehicle the detection system is to be used on. 
Ensure Particle Argon is securely mounted on board the vehicle and wire the sensor to the device through use of a miniature breadboard. 
Wire the VCC pin from the sensor to the 5V pin of the voltage converter. 
Wire the 3.3V pin on the voltage converter to the 3.3V pin on Argon and the GND pin to the Argon GND pin. 
Wire the GND pin on the sensor to GND on the Argon and the data pin to pin A1. 
Plug in the power supply.

Central System:
The central system should be set up on a Raspberry Pi. 
Set up the 4-channel relay bank near the Raspberry Pi and supply 5 volts to the VCC pin and GND to a Ground pin on the Raspberry Pi. 
Wire the forward relay IN to GPIO02, the back relay IN to GPIO03, the left relay IN to GPIO04 and the right relay IN to GPIO17. 
This next part will vary dependent on the vehicle being controlled. 
For this prototype, this required the circuit board used within the controller. 
Work out how the remote takes input and use the relays to simulate. 
Again, for this prototype, this required completing a circuit to achieve each output. 
To simulate this required soldering wires to parts of the board then running these wires to common and normally open contact on each relay. 
In this way when a relay closes it will complete a circuit and the controller will send the related command to the remote-controlled car. 
Wire buzzer active pin to GPIO18 and the negative pin to GND. 
Ensure Raspberry Pi is set up with NOOBS operating system and plug in to the power supply.
