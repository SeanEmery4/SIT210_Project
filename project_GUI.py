# Libaries
from tkinter import *
import tkinter.font
import RPi.GPIO as GPIO
from time import sleep
import requests, json
from threading import Thread

GPIO.setmode(GPIO.BCM)

#Disable warnings
GPIO.setwarnings(False)

## GUI set up
win = Tk()
win.title("Obstacle Detection System")

headingFont = tkinter.font.Font(family = 'Helvetica', size = 15, weight = "bold")
SubheadingFont = tkinter.font.Font(family = 'Helvetica', size = 12, weight = "bold")

canvas = Canvas(win, width = 715, height = 410)
canvas.pack()

## Variables
global mode
global F_C_Dist_GUI
global DetectButtonGUI
global AutoButtonGUI
global ManualButtonGUI
global OffButtonGUI
global ModeDescGUI
global F_C_Object_GUI

## Functions

def getDistance():
    responce = requests.get('https://api.particle.io/v1/devices/e00fce6825acdbf3eaef2482/F_C_Dist?access_token=05a78f428e275ea748d57326857802757ed4ead0')
    respJSON = responce.json()
    
    try:
        dist = int(respJSON.get("result"))
        return dist
    except:
        return "Error"

def writeData(F_C_Dist):
    global F_C_Dist_GUI, F_C_Object_GUI
    
    try:
        canvas.delete(F_C_Dist_GUI, F_C_Object_GUI)
    except:
        pass
    
    F_C_Dist_Str = "{dist}cm".format(dist = F_C_Dist)
    
    if F_C_Dist == "Error":
        F_C_Dist_GUI = canvas.create_text(100, 350, font = SubheadingFont, fill = 'red', text = F_C_Dist)
    elif F_C_Dist <= 80 and F_C_Dist >= 50:
        F_C_Object_GUI = canvas.create_rectangle(405, 40, 445, 105, fill = 'orange', outline = 'orange')
        F_C_Dist_GUI = canvas.create_text(100, 350, font = SubheadingFont, fill = 'red', text = F_C_Dist_Str)
    elif F_C_Dist < 50:
        F_C_Object_GUI = canvas.create_rectangle(405, 40, 445, 105, fill = 'red', outline = 'red')
        F_C_Dist_GUI = canvas.create_text(100, 350, font = SubheadingFont, fill = 'red', text = F_C_Dist_Str)
    else:
        F_C_Dist_GUI = canvas.create_text(100, 350, font = SubheadingFont, fill = 'green', text = "Clear")


def system():
    global F_C_Dist_GUI, F_C_Object_GUI, mode
    
    while True:
        F_C_Dist = getDistance()
        
        if mode == 0:
            pass
        else:
            writeData(F_C_Dist)
        
    
def setCanvas():
   
    #create sections
    canvas.create_rectangle(3, 3, 712, 37, fill = 'grey65', outline = 'grey60')
    canvas.create_rectangle(3, 43, 177, 290, fill = 'grey65', outline = 'grey60')
    canvas.create_rectangle(3, 300, 177, 400, fill = 'grey65', outline = 'grey60')
    
    # create heading
    canvas.create_text(360, 20, font = headingFont, text = "Obstacle Detection System")
    canvas.create_text(40, 57, font = SubheadingFont, text = "Mode:")
    
    # create data section
    canvas.create_text(70, 315, font = SubheadingFont, text = "Obstacle Data")
    canvas.create_text(40, 350, font = SubheadingFont, text = "Front: ")
    canvas.create_text(41, 375, font = SubheadingFont, text = "Rear: ")
    
    #create car
    canvas.create_rectangle(350, 110, 500, 360, fill = 'blue2', outline = 'blue') #body
    canvas.create_rectangle(360, 170, 490, 220, fill = 'black') # windscreen
    canvas.create_rectangle(360, 260, 490, 350, fill = 'blue4', outline = 'blue4') #tray
    canvas.create_rectangle(310, 120, 348, 190, fill = 'black') #FLtyre
    canvas.create_rectangle(502, 120, 540, 190, fill = 'black') #FRtyre
    canvas.create_rectangle(310, 270, 348, 340, fill = 'black') #RLtyre
    canvas.create_rectangle(502, 270, 540, 340, fill = 'black') #RRtyre

def drawDetectButton(onOff):
    global DetectButtonGUI
    
    if onOff == "on":
        DetectButtonGUI = canvas.create_window(90, 97, window = DetectModeOnButton)
    else:
        DetectButtonGUI = canvas.create_window(90, 97, window = DetectModeOffButton)

def drawAutoButton(onOff):
    global AutoButtonGUI
    
    if onOff == "on":
        AutoButtonGUI = canvas.create_window(90, 147, window = AutoModeOnButton)
    else:
        AutoButtonGUI = canvas.create_window(90, 147, window = AutoModeOffButton)

def drawManButton(onOff):
    global ManualButtonGUI
    
    if onOff == "on":
        ManualButtonGUI = canvas.create_window(90, 197, window = ManModeOnButton)
    else:
        ManualButtonGUI = canvas.create_window(90, 197, window = ManModeOffButton)

def drawOffButton():
    global OffButtonGUI
    
    OffButtonGUI = canvas.create_window(90, 247, window = OffModeButton)

def setDataOn():
    ## call get distance and write data when indirect addressing is done
    pass


def setModeOff():
    global mode
    global ModeDescGUI
    
    mode = 0
    
    # clear canvas to redraw
    canvas.delete(DetectButtonGUI, AutoButtonGUI, ManualButtonGUI, OffButtonGUI, ModeDescGUI, F_C_Dist_GUI, F_C_Object_GUI)
    
    drawDetectButton("off")
    drawAutoButton("off")
    drawManButton("off")
    drawOffButton()
    ModeDescGUI = canvas.create_text(80, 57, font = SubheadingFont, text = "Off")
  
def setModeDetect():
    global mode
    global ModeDescGUI
    
    mode = 1
    
    canvas.delete(DetectButtonGUI, AutoButtonGUI, ManualButtonGUI, OffButtonGUI, ModeDescGUI)
    
    drawDetectButton("on")
    drawAutoButton("off")
    drawManButton("off")
    drawOffButton()
    ModeDescGUI = canvas.create_text(105, 57, font = SubheadingFont, text = "Detection")
    
def setModeAuto():
    global mode
    global ModeDescGUI
    
    mode = 2
    
    canvas.delete(DetectButtonGUI, AutoButtonGUI, ManualButtonGUI, OffButtonGUI, ModeDescGUI)

    drawDetectButton("off")
    drawAutoButton("on")
    drawManButton("off")
    drawOffButton()
    ModeDescGUI = canvas.create_text(118, 57, font = SubheadingFont, text = "Autonomous")
   
def setModeMan():
    global mode
    global ModeDescGUI
    
    mode = 3
    
    canvas.delete(DetectButtonGUI, AutoButtonGUI, ManualButtonGUI, OffButtonGUI, ModeDescGUI)

    drawDetectButton("off")
    drawAutoButton("off")
    drawManButton("on")
    drawOffButton()
    ModeDescGUI = canvas.create_text(95, 57, font = SubheadingFont, text = "Manual")
   
def close():
    GPIO.cleanup()
    win.destroy()

    
if __name__ == "__main__":
    ## Widgets
    DetectModeOffButton = Button(win, text = "Detection Mode", command = setModeDetect, bg = 'orange', height = 2, width = 15)
    DetectModeOnButton = Button(win, text = "Detection Mode", command = setModeDetect, bg = 'green', height = 2, width = 15)
    
    AutoModeOffButton = Button(win, text = "Autonomous Mode", command = setModeAuto, bg = 'orange', height = 2, width = 15)
    AutoModeOnButton = Button(win, text = "Autonomous Mode", command = setModeAuto, bg = 'green', height = 2, width = 15)
    
    ManModeOffButton = Button(win, text = "Manual Mode", command = setModeMan, bg = 'orange', height = 2, width = 15)
    ManModeOnButton = Button(win, text = "Manual Mode", command = setModeMan, bg = 'green', height = 2, width = 15)
    
    OffModeButton = Button(win, text = "System Off", command = setModeOff, bg = 'red', height = 2, width = 15)
    
    setCanvas()
    mode = 0
    drawDetectButton("off")
    drawAutoButton("off")
    drawManButton("off")
    drawOffButton()
    ModeDescGUI = canvas.create_text(80, 57, font = SubheadingFont, text = "Off")
    
    F_C_Object_GUI = canvas.create_rectangle(0, 0, 0, 0)
    
    systemThread = Thread(target = system)
    systemThread.start()
    
    win.protocol("WM_DELETE_WINDOW", close)

    win.mainloop()
    
