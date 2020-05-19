## Libaries
from tkinter import *
import tkinter.font
import RPi.GPIO as GPIO
from time import sleep
import requests, json
from threading import Thread, Lock
import paho.mqtt.client as mqtt

#set pin mode
GPIO.setmode(GPIO.BCM)

#Disable warnings
GPIO.setwarnings(False)

## Global Variables
global win, canvas, headingFont, SubheadingFont #GUI Setup variables
global mode, F_C_Dist  #vairables used across threads
global DetectButtonGUI, AutoButtonGUI, ManualButtonGUI, OffButtonGUI #Mode button variables
global ForButtonGUI, BackButtonGUI, LeftButtonGUI, RightButtonGUI #Manual button variables
global Cont_Panel, Cont_Panel_Heading #Control panel variables
global ModeDescGUI, F_C_Dist_GUI, F_C_Object_GUI
forwardOnFeedback = False
DetectOn = False
F_C_Dist = "Error" #start F_C_Dist as error incase can't connect to on-board system

#GPIO pins for relays and buzzer
forwardPin = 2
backPin = 3
leftPin = 4
rightPin = 17
buzzer = 18

# set up lock for when two threads access same variable
data_lock = Lock()

## Functions

# GUI set up
def InitGUI():
    global win, canvas, headingFont, SubheadingFont #gloabl variables that require changing
    
    win = Tk()
    win.title("Obstacle Detection System")

    headingFont = tkinter.font.Font(family = 'Helvetica', size = 15, weight = "bold")
    SubheadingFont = tkinter.font.Font(family = 'Helvetica', size = 12, weight = "bold")

    canvas = Canvas(win, width = 715, height = 410)
    canvas.pack()

def messageFunction(client, userdata, message):
    global F_C_Dist
    message = str(message.payload.decode("utf-8"))
    
    try:
        F_C_Dist = int(message)
    except:
        F_C_Dist = message
 
def onConnectFunction(client, userdata, flags, rc):
    if rc == 0:
        print("Connection Established")
        
def onDisconnectFunction(client, userdata, rc):
    global F_C_Dist
    F_C_Dist = "Error"

def InitMQTT():
    
    ourClient = mqtt.Client("SIT210_SE_MQTT_Pi") # Create a MQTT client object
    ourClient.connect("test.mosquitto.org", 1883) # Connect to the test MQTT broker
    ourClient.subscribe("F_C_Distance_Log") # Subscribe to log from particle
    ourClient.on_connect = onConnectFunction
    ourClient.on_message = messageFunction      # Attach the messageFunction to subscription
    ourClient.on_disconnect = onDisconnectFunction
    
    ourClient.loop_start()

# Set relay pins as outputs
def setup():
    GPIO.setup(forwardPin, GPIO.OUT)
    GPIO.setup(backPin, GPIO.OUT)
    GPIO.setup(leftPin, GPIO.OUT)
    GPIO.setup(rightPin, GPIO.OUT)
    GPIO.setup(buzzer, GPIO.OUT)

def detectModeSystem():
    global F_C_Dist, mode, forwardOnFeedback, DetectOn #global variables neded
    
    DetectOn = True # set detect bool on so as not only have one active thread
    
    print("Detect Mode Start")
    
    # while loop to continute until detect mode is changed
    while mode == 2:
        # try as when system is first starting up may take some time to get F_C_Dist
        try:
            # if F_C_Dist is a string and therefore an Error draw users attention
            if isinstance(F_C_Dist, str):
                GPIO.output(buzzer, GPIO.HIGH)
                sleep(0.3)
                GPIO.output(buzzer, GPIO.LOW)
                
            # if distance is under 80 and forward is on alert user to obstacle ahead    
            elif F_C_Dist <= 80 and forwardOnFeedback is True:
                GPIO.output(buzzer, GPIO.HIGH)
                sleep(0.5)
                GPIO.output(buzzer, GPIO.LOW)
                sleep(0.4)
            # if no error or obstacle turn buzzer off
            else:
                GPIO.output(buzzer, GPIO.LOW)
        except:
            print("Detect System not yet ready")
            sleep(0.5)
            
        sleep(0.1)
    
    # set detectOn to false so system knows no thread is running
    DetectOn = False
    print("Detect Mode End")

# Funtion to turn forward pin on
def forwardOn(event):
    global forwardOnFeedback, DetectOn
    
    GPIO.output(forwardPin, GPIO.HIGH)
    
    forwardOnFeedback = True # let system no forward is on
    DetectSystemThread = Thread(target = detectModeSystem) # set up thread for detection mode buzzer
    
    # if forward is turned on in detect mode need to start thread
    # also check no detect thread is already running
    if mode == 2 and DetectOn is False:
        DetectSystemThread.start()
   
# Funtion to turn forward pin off
def forwardOff(event):
    global forwardOnFeedback
    
    GPIO.output(forwardPin, GPIO.LOW)
    # let system know forward is no longer on and turn buzzer off
    forwardOnFeedback = False
    GPIO.output(buzzer, GPIO.LOW)

# Funtion to turn back pin on
def backOn(event):
    GPIO.output(backPin, GPIO.HIGH)
    
# Funtion to turn back pin off
def backOff(event):
    GPIO.output(backPin, GPIO.LOW)
    
# Funtion to turn left pin on
def leftOn():
    GPIO.output(leftPin, GPIO.HIGH)
    
# Funtion to turn left pin off
def leftOff():
    GPIO.output(leftPin, GPIO.LOW)
    
# Funtion to turn right pin on
def rightOn():
    GPIO.output(rightPin, GPIO.HIGH)
    
# Funtion to turn right pin off
def rightOff():
    GPIO.output(rightPin, GPIO.LOW)
    
# Function to turn all motion off
def motionOff():
    forwardOff("off")
    backOff("off")
    leftOff()
    rightOff()
    
    
# function to write ditance data and display to GUI
def writeData(F_C_Dist):
    global F_C_Dist_GUI, F_C_Object_GUI # variables to write to
    
    # try delete GUI features if they've been initiated
    try:
        canvas.delete(F_C_Dist_GUI, F_C_Object_GUI)
    except:
        pass
    
    # concatinate distance returned with cm
    F_C_Dist_Str = "{dist}cm".format(dist = F_C_Dist)
    
    # if no value has been returned and system is in error state notify user
    if F_C_Dist == "Error":
        F_C_Dist_GUI = canvas.create_text(100, 350, font = SubheadingFont, fill = 'red', text = F_C_Dist)
    elif F_C_Dist <= 80 and F_C_Dist >= 50:
        # if system detects something between 50 and 80cm display figure and object in orange
        F_C_Object_GUI = canvas.create_arc(305, 40, 485, 170, start = 60, extent = 60, fill = 'orange', outline = 'orange')
        F_C_Dist_GUI = canvas.create_text(100, 350, font = SubheadingFont, fill = 'red', text = F_C_Dist_Str)
    elif F_C_Dist < 50:
        # if system detects something less than 50cm away display figure and object in red
        F_C_Object_GUI = canvas.create_arc(305, 40, 485, 170, start = 60, extent = 60, fill = 'red', outline = 'red')
        F_C_Dist_GUI = canvas.create_text(100, 350, font = SubheadingFont, fill = 'red', text = F_C_Dist_Str)
    else:
        # if nothing detected and system not in error, display clear
        F_C_Dist_GUI = canvas.create_text(100, 350, font = SubheadingFont, fill = 'green', text = "Clear")

# function to loop on seperate thread constantly measuring front distance and updating GUI
def ObjectDetectionSystem():
    global mode, F_C_Dist #variables to be monitored and changed
    
    # infinite loop
    while True:
                
        # if mode is off do not display data
        if (mode == 0 or mode == 1):
            pass
        else:
            # any other mode display data
            writeData(F_C_Dist)
            
        sleep(0.5)
        
# function to set canvas at start up
def setCanvas():
    global F_C_Object_GUI, F_C_Dist_GUI
    
    #create sections
    canvas.create_rectangle(3, 3, 712, 37, fill = 'grey65', outline = 'grey60')
    canvas.create_rectangle(3, 43, 177, 290, fill = 'grey65', outline = 'grey60')
    canvas.create_rectangle(3, 300, 177, 400, fill = 'grey65', outline = 'grey60')
    
    # create headings
    canvas.create_text(360, 20, font = headingFont, text = "Obstacle Detection System")
    canvas.create_text(40, 57, font = SubheadingFont, text = "Mode:")
    canvas.create_text(70, 315, font = SubheadingFont, text = "Obstacle Data")
    
    # create data section
    canvas.create_text(40, 350, font = SubheadingFont, text = "Front: ")
    #canvas.create_text(41, 375, font = SubheadingFont, text = "Rear: ")
    
    #create car
    canvas.create_rectangle(320, 110, 470, 360, fill = 'blue2', outline = 'blue') #body
    canvas.create_rectangle(330, 170, 460, 220, fill = 'black') # windscreen
    canvas.create_rectangle(330, 260, 460, 350, fill = 'blue4', outline = 'blue4') #tray
    canvas.create_rectangle(280, 120, 318, 190, fill = 'black') #FLtyre
    canvas.create_rectangle(472, 120, 510, 190, fill = 'black') #FRtyre
    canvas.create_rectangle(280, 270, 318, 340, fill = 'black') #RLtyre
    canvas.create_rectangle(472, 270, 510, 340, fill = 'black') #RRtyre
    
    F_C_Object_GUI = canvas.create_rectangle(0, 0, 0, 0)
    F_C_Dist_GUI = ""

def setLeftControls(onOff):
    global LeftButtonGUI
    
    # try delete current button to be replaced
    try:
        canvas.delete(LeftButtonGUI)
    except:
        pass
    
    # set on button if on, else set off button
    if onOff == "on":
        LeftButtonGUI = canvas.create_window(567, 135, window = LeftOnButton)
        setRightControls("off")
        sleep(0.1)
        leftOn()
    else:
        LeftButtonGUI = canvas.create_window(567, 135, window = LeftOffButton)
        leftOff()

def setRightControls(onOff):
    global RightButtonGUI
    
    # try delete current button to be replaced
    try:
        canvas.delete(RightButtonGUI)
    except:
        pass
    
    # set on button if on, else set off button
    if onOff == "on":
        RightButtonGUI = canvas.create_window(684, 135, window = RightOnButton)
        setLeftControls("off")
        sleep(0.1)
        rightOn()
    else:
        RightButtonGUI = canvas.create_window(684, 135, window = RightOffButton)
        rightOff()

def clearControlsPanel():
    try:
        canvas.delete(Cont_Panel, Cont_Panel_Heading, ForButtonGUI, BackButtonGUI, LeftButtonGUI, RightButtonGUI)
    except:
        pass

# function to draw control panel and buttons when in certain modes
def drawControlsPanel():
    global Cont_Panel, Cont_Panel_Heading, ForButtonGUI, BackButtonGUI, LeftButtonGUI, RightButtonGUI
    
    clearControlsPanel()
    
    # create control panel with heading
    Cont_Panel = canvas.create_rectangle(538, 43, 712, 200, fill = 'grey65', outline = 'grey60')
    Cont_Panel_Heading = canvas.create_text(625, 57, font = SubheadingFont, text = "Manual Controls")

    # create buttons
    ForButtonGUI = canvas.create_window(625, 110, window = ForwardButton)
    BackButtonGUI = canvas.create_window(625, 161, window = BackButton)
    LeftButtonGUI = canvas.create_window(567, 135, window = LeftOffButton)
    RightButtonGUI = canvas.create_window(684, 135, window = RightOffButton)

# function to draw detect button in whatever mode is passed
def drawDetectButton(onOff):
    global DetectButtonGUI
    
    # try delete current button to be replaced
    try:
        canvas.delete(DetectButtonGUI)
    except:
        pass
    
    # set on button if on, else set off button
    if onOff == "on":
        DetectButtonGUI = canvas.create_window(90, 147, window = DetectModeOnButton)
    else:
        DetectButtonGUI = canvas.create_window(90, 147, window = DetectModeOffButton)

# function to draw auto button in whatever mode is passed
def drawAutoButton(onOff):
    global AutoButtonGUI
    
    # try delete current button to be replaced
    try:
        canvas.delete(AutoButtonGUI)
    except:
        pass
    
    # set on button if on, else set off button
    if onOff == "on":
        AutoButtonGUI = canvas.create_window(90, 97, window = AutoModeOnButton)
    else:
        AutoButtonGUI = canvas.create_window(90, 97, window = AutoModeOffButton)

# function to draw manual button in whatever mode is passed
def drawManButton(onOff):
    global ManualButtonGUI
    
    # try delete current button to be replaced
    try:
        canvas.delete(ManualButtonGUI)
    except:
        pass
    
    # set on button if on, else set off button
    if onOff == "on":
        ManualButtonGUI = canvas.create_window(90, 197, window = ManModeOnButton)
    else:
        ManualButtonGUI = canvas.create_window(90, 197, window = ManModeOffButton)

# function to draw off button
def drawOffButton():
    global OffButtonGUI
    
    # try delete current button to be replaced
    try:
        canvas.delete(OffButtonGUI)
    except:
        pass
    
    # set button
    OffButtonGUI = canvas.create_window(90, 247, window = OffModeButton)


# sets mode to off and updates GUI
def setModeOff():
    global mode, ModeDescGUI, stopAutoThread
    
    # Ensure all relayes are turned off when shifting modes
    motionOff()
        
    # set mode to 0 for off
    with data_lock: mode = 0
    
    # clear canvas to redraw
    try:
        canvas.delete(ModeDescGUI)
        canvas.delete(F_C_Dist_GUI)
        canvas.delete(F_C_Object_GUI)
    except:
        pass
    
    # call draw buttons function all in the off state
    clearControlsPanel()
    drawDetectButton("off")
    drawAutoButton("off")
    drawManButton("off")
    drawOffButton()
    
    # update mode description to off
    ModeDescGUI = canvas.create_text(80, 57, font = SubheadingFont, text = "Off")

# sets mode to manual and updates GUI
def setModeMan():
    global mode, ModeDescGUI, stopAutoThread
    
    # Ensure all relayes are turned off when shifting modes
    motionOff()
        
    # set mode to 3 for manual
    with data_lock: mode = 1
    
    # clear canvas to update
    try:
        canvas.delete(ModeDescGUI)
        canvas.delete(F_C_Dist_GUI)
        canvas.delete(F_C_Object_GUI)
    except:
        pass

    # draw buttons in relevant states and control panel
    drawControlsPanel()
    drawDetectButton("off")
    drawAutoButton("off")
    drawManButton("on")
    drawOffButton()

    # update mode decription
    ModeDescGUI = canvas.create_text(95, 57, font = SubheadingFont, text = "Manual")
  
 
# sets mode to detect and updates GUI
def setModeDetect():
    global mode, ModeDescGUI, stopAutoThread
    
    # Ensure all relayes are turned off when shifting modes
    motionOff()
    
    # set mode to 1 for detect
    with data_lock: mode = 2
    
    # clear canvas components to be replaced
    canvas.delete(ModeDescGUI)
    
    # draw buttons and control panel in relevant states
    drawControlsPanel()
    drawDetectButton("on")
    drawAutoButton("off")
    drawManButton("off")
    drawOffButton()
       
    # update mode description
    ModeDescGUI = canvas.create_text(105, 57, font = SubheadingFont, text = "Detection")
    

def AutonomousSystem():
    global stopAutoThread
    forwardOff("off")
    
    # while loop to continue while autonomous mode is on
    while mode == 3:
        # try to use data to control vehicle, if theres an error turn all relays off
        try:
            if F_C_Dist == "Error" or F_C_Dist < 80:
                print('STOP')
                forwardOff('off')
            #elif F_C_Dist < 80:
            #    print('STOP')
            #    forwardOff('off')
            elif F_C_Dist >=81:
                print('GO')
                forwardOn('on')
        except:
            motionOff()
            sleep(0.1)
            
        sleep(0.1)
            
    print('Auto Thread Off')
    motionOff() # turn all motion off when exiting mode

# sets mode to autonomous and updates GUI
def setModeAuto():
    global mode, ModeDescGUI, stopAutoThread
    
    # Ensure all relayes are turned off when shifting modes
    motionOff()
       
    # update mode to 2 for autonomous
    with data_lock: mode = 3
    
    # clear canvas to update
    canvas.delete(ModeDescGUI)
    
    # draw buttons in relevant states
    clearControlsPanel()
    drawDetectButton("off")
    drawAutoButton("on")
    drawManButton("off")
    drawOffButton()
    
    #stopAutoThread = False
    AutonomousSystemThread = Thread(target = AutonomousSystem)
    AutonomousSystemThread.start()
    
    # update mode description
    ModeDescGUI = canvas.create_text(118, 57, font = SubheadingFont, text = "Autonomous")
   
   
# function to set widgets called once at the start
def setWidgets():
    global DetectModeOffButton, DetectModeOnButton, AutoModeOffButton, AutoModeOnButton
    global ManModeOffButton, ManModeOnButton, OffModeButton
    global ForwardButton, BackButton, LeftOffButton, LeftOnButton, RightOffButton, RightOnButton
    
    DetectModeOffButton = Button(win, text = "Detection Mode", command = setModeDetect, bg = 'orange', height = 2, width = 15)
    DetectModeOnButton = Button(win, text = "Detection Mode", bg = 'green', height = 2, width = 15)
    
    AutoModeOffButton = Button(win, text = "Autonomous Mode", command = setModeAuto, bg = 'orange', height = 2, width = 15)
    AutoModeOnButton = Button(win, text = "Autonomous Mode", bg = 'green', height = 2, width = 15)
    
    ManModeOffButton = Button(win, text = "Manual Mode", command = setModeMan, bg = 'orange', height = 2, width = 15)
    ManModeOnButton = Button(win, text = "Manual Mode", bg = 'green', height = 2, width = 15)
    
    OffModeButton = Button(win, text = "System Off", command = setModeOff, bg = 'red', height = 2, width = 15)
    
    LeftOffButton = Button(win, text = "Left", command = lambda: setLeftControls("on"), activebackground = 'green', height = 5, width = 2)
    LeftOnButton = Button(win, text = "Left", command = lambda: setLeftControls("off"), bg = 'green', height = 5, width = 2)

    RightOffButton = Button(win, text = "Right", command = lambda: setRightControls("on"), activebackground = 'green', height = 5, width = 2)
    RightOnButton = Button(win, text = "Right", command = lambda: setRightControls("off"), bg = 'green', height = 5, width = 2)
    
    ForwardButton = Button(win, text = "Forward", activebackground = 'green', height = 2, width = 4)
    ForwardButton.bind('<ButtonPress-1>', forwardOn)
    ForwardButton.bind('<ButtonRelease-1>', forwardOff)
    
    BackButton = Button(win, text = "Back", activebackground = 'green', height = 2, width = 4)
    BackButton.bind('<ButtonPress-1>', backOn)
    BackButton.bind('<ButtonRelease-1>', backOff)
    
      
# method called at the end to clean up GPIO and destroy window
def close():
    setModeOff()
    GPIO.cleanup()
    win.destroy()

    
## Main method starting point
if __name__ == "__main__":
    
    #Initate GUI variables
    InitGUI() 
    
    #Initiate MQTT connection
    InitMQTT()
    
    #Iniciate GPIO pins required
    setup()
    
    #Set up widgets
    setWidgets()
    
    # set up canvas with sections and car
    setCanvas()
    
    # set starting mode to off state
    setModeOff()
    
    # start thread for object detection system
    # this system just reads data from argon and updates variable and displays on GUI
    ObjectDetectionSystemThread = Thread(target = ObjectDetectionSystem)
    ObjectDetectionSystemThread.start()
    
    win.protocol("WM_DELETE_WINDOW", close)

    #Thread to deal with button push events
    win.mainloop()
    
