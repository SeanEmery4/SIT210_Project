# SIT210_Project
This folder contains source code for my project for SIT210 - Embedded Systems Development project.
This prototype is for an obstace detection system on a remote controlled car.
The on board system contains a Sharp IR sensor and Particle Argon.
The central system is a raspberry pi with a GUI, 4 relay bank and buzzer.
Communication between the two is through MQTT.


Hardware Required:

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


On-Board System Set Up:

Ensure the IR distance sensor is mounted securely to the front of the vehicle the detection system is to be used on. 
Ensure Particle Argon is securely mounted on board the vehicle and wire the sensor to the device through use of a miniature breadboard. 
Wire the VCC pin from the sensor to the 5V pin of the voltage converter. 
Wire the 3.3V pin on the voltage converter to the 3.3V pin on Argon and the GND pin to the Argon GND pin. 
Wire the GND pin on the sensor to GND on the Argon and the data pin to pin A1. 
Plug in the power supply.
Ensure the firmware for Particle Argon is downloaded from this repo and successfully flashed to the device.


Central System Set Up:

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
Ensure Python software from this repo is downloaded and opened in an IDE on the Raspberry Pi.


User Manual:

Run the code on the Raspberry Pi and wait for the user interface to appear in a window. 
The system should be in the off mode. This can be seen by the fact that none of the other mode’s buttons are green, the description ‘Off’ is displayed at the top of the mode panel and that there is no data being displayed in the data panel at the bottom right.
To control the car from the GUI without any detection, press the manual button. 
The system will shift into this mode as seen by the manual button being coloured green, the mode description being “Manual’ and the controls panel appearing in the top right. 
To move the car forward, click and hold the forward button on. To stop, release the forward button. 
Reverse operates in the same way but by pressing the back button. 
To turn left, click on the left button. 
This will turn the wheels left and hold them there until the left button is clicked again or the right button is clicked. 
This is to ensure that both the right and left relays are never on at the same time. 
The right button operates in the same way. 

To add some detection readings into the manual mode, click the detect button. 
The system will have moved into detect mode, which can be seen by this mode button being green, the mode description being ‘Detect’ and the data panel now being populated with either a distance to an object or ‘Clear’. 
To control the vehicle in this system, follow the manual instructions. 
In the detect mode however, if an object is detected in front of the vehicle it will be shown through a red or orange cone in front of the vehicle on the GUI. 
The distance to the object will be displayed in the data panel and a buzzer will be heard while the car is moving forward and an object is detected. 
This is to draw the user’s attention to the obstruction.

To use the system in the autonomous mode, press the autonomous button. 
Again, the button will go green, the mode description will be ‘Autonomous’ and the manual controls will no longer be available. 
The system will now drive forward provided the on-board system does not detect an obstacle. 
Once an object is present, the forward motion stops. 
The forward motion will also be stopped if the Raspberry Pi cannot read the data from the on-board system. 
This is a safety precaution, so the vehicle is not driving blind.
