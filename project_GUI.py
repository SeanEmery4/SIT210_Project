## Libaries
from tkinter import *
import tkinter.font
import RPi.GPIO as GPIO
from time import sleep
import requests, json
from threading import Thread, Lock
from functools import partial

#set pin mode
GPIO.setmode(GPIO.BCM)

#Disable warnings
GPIO.setwarnings(False)

## Global Variables
global win, canvas, headingFont, SubheadingFont #GUI Setup variables
global mode, F_C_Dist #vairables used across threads
global DetectButtonGUI, AutoButtonGUI, ManualButtonGUI, OffButtonGUI #Mode button variables
global ForButtonGUI, BackButtonGUI, LeftButtonGUI, RightButtonGUI #Manual button variables
global Cont_Panel, Cont_Panel_Heading #Control panel variables
global ModeDescGUI, F_C_Dist_GUI, F_C_Object_GUI
stopAutoThread = True

#GPIO pins for relays
forwardPin = 2
backPin = 3
leftPin = 4
rightPin = 17

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

# Set relay pins as outputs
def setup():
    GPIO.setup(forwardPin, GPIO.OUT)
    GPIO.setup(backPin, GPIO.OUT)
    GPIO.setup(leftPin, GPIO.OUT)
    GPIO.setup(rightPin, GPIO.OUT)

# Funtion to turn forward pin on
def forwardOn(event):
    GPIO.output(forwardPin, GPIO.HIGH)
   
# Funtion to turn forward pin off
def forwardOff(event):
    GPIO.output(forwardPin, GPIO.LOW)

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
    
def motionOff():
    forwardOff("off")
    backOff("off")
    leftOff()
    rightOff()
    
# function to get distance from argon and return the value
def getFrontDistance():
    # requests is very slow, hard real time issue, try bluetooth
    responce = requests.get('https://api.particle.io/v1/devices/e00fce6825acdbf3eaef2482/F_C_Dist?access_token=05a78f428e275ea748d57326857802757ed4ead0')
    respJSON = responce.json()
    
    # try get distance returned as an int and return
    try:
        dist = int(respJSON.get("result"))
        return dist
    except:
        return "Error"

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
def DetectionSystem():
    global mode, F_C_Dist #variables to be monitored and changed
    
    # infinite loop
    while True:
        # get distance from argon and store in F_C_Dist
        F_C_Dist = getFrontDistance()
        
        # if mode is off do not display data
        if (mode == 0 or mode == 1):
            pass
        else:
            # any other mode display data
            writeData(F_C_Dist)
        
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
    canvas.create_text(41, 375, font = SubheadingFont, text = "Rear: ")
    
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
    
    motionOff()
    stopAutoThread = True
    
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
    
    motionOff()
    stopAutoThread = True
    
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
    
    motionOff()
    stopAutoThread = True
    
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
    
    while True:
        try:
            if F_C_Dist == "Error":
                print('STOP')
                forwardOff('off')
            elif F_C_Dist < 80:
                print('STOP')
                forwardOff('off')
            elif F_C_Dist >=81:
                print('GO')
                forwardOn('on')
        except:
            motionOff()
            sleep(2)
            
        sleep(0.1)
        
        if stopAutoThread:
            print('Auto Thread Off')
            motionOff()
            break

# sets mode to autonomous and updates GUI
def setModeAuto():
    global mode, ModeDescGUI, stopAutoThread
    
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
    
    stopAutoThread = False
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
    GPIO.cleanup()
    win.destroy()

    
## Main method starting point
if __name__ == "__main__":
    
    #Initate GUI variables
    InitGUI() 
    
    #Iniciate GPIO pins required
    setup()
    
    #Set up widgets
    setWidgets()
    
    # set up canvas with sections and car
    setCanvas()
    
    # set starting mode to off state
    setModeOff()
    
    # start thread for detection system
    # this system just reads data from argon and updates variable and displays on GUI
    DetectionSystemThread = Thread(target = DetectionSystem)
    DetectionSystemThread.start()
    
    win.protocol("WM_DELETE_WINDOW", close)

    #Thread to deal with button push events
    win.mainloop()
