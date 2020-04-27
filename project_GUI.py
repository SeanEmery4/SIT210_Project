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

## GUI
win = Tk()
win.title("Obstacle Detection System")
headingFont = tkinter.font.Font(family = 'Helvetica', size = 15, weight = "bold")
SubheadingFont = tkinter.font.Font(family = 'Helvetica', size = 12, weight = "bold")
canvas = Canvas(win, width = 715, height = 410)
canvas.pack()

## Variables
global mode

## Functions

def getDistance():
    responce = requests.get('https://api.particle.io/v1/devices/e00fce6825acdbf3eaef2482/F_C_Dist?access_token=05a78f428e275ea748d57326857802757ed4ead0')
    respJSON = responce.json()
    dist = respJSON.get("result")
    return dist

def system():
    F_C_Dist = getDistance()
    canvas.create_text(100, 350, font = SubheadingFont, text = F_C_Dist)
    
def setCanvas():
    # clear cnavas to redraw
    canvas.delete("all")
    
    #create sections
    canvas.create_rectangle(3, 3, 712, 37, fill = 'grey65', outline = 'grey60')
    canvas.create_rectangle(3, 43, 177, 230, fill = 'grey65', outline = 'grey60')
    canvas.create_rectangle(3, 300, 177, 400, fill = 'grey65', outline = 'grey60')
    # create heading
    canvas.create_text(360, 20, font = headingFont, text = "Obstacle Detection System")
    canvas.create_text(40, 57, font = SubheadingFont, text = "Mode:")
    # create data section
    canvas.create_text(70, 315, font = SubheadingFont, text = "Obstacle Data")
    canvas.create_text(40, 350, font = SubheadingFont, text = "Front: ")
    system()
    canvas.create_text(41, 375, font = SubheadingFont, text = "Rear: ")
    #create car
    canvas.create_rectangle(350, 110, 500, 360, fill = 'blue2', outline = 'blue') #body
    canvas.create_rectangle(360, 170, 490, 220, fill = 'black') # windscreen
    canvas.create_rectangle(360, 260, 490, 350, fill = 'blue4', outline = 'blue4') #tray
    canvas.create_rectangle(310, 120, 348, 190, fill = 'black') #FLtyre
    canvas.create_rectangle(502, 120, 540, 190, fill = 'black') #FRtyre
    canvas.create_rectangle(310, 270, 348, 340, fill = 'black') #RLtyre
    canvas.create_rectangle(502, 270, 540, 340, fill = 'black') #RRtyre


def setModeOff():
    mode = 0
    setCanvas()
    canvas.create_window(90, 97, window = DetectModeOffButton)
    canvas.create_window(90, 147, window = AutoModeOffButton)
    canvas.create_window(90, 197, window = OffModeButton)
    canvas.create_text(80, 57, font = SubheadingFont, text = "Off")
  
def setModeDetect():
    mode = 1
    setCanvas()
    canvas.create_window(90, 97, window = DetectModeOnButton)
    canvas.create_window(90, 147, window = AutoModeOffButton)
    canvas.create_window(90, 197, window = OffModeButton)
    canvas.create_text(105, 57, font = SubheadingFont, text = "Detection")
    
def setModeAuto():
    mode = 1
    setCanvas()
    canvas.create_window(90, 97, window = DetectModeOffButton)
    canvas.create_window(90, 147, window = AutoModeOnButton)
    canvas.create_window(90, 197, window = OffModeButton)
    canvas.create_text(120, 57, font = SubheadingFont, text = "Autonomous")
   
def close():
    GPIO.cleanup()
    win.destroy()

    
    
## Widgets
setCanvas()
DetectModeOffButton = Button(win, text = "Detection Mode", command = setModeDetect, bg = 'orange', height = 2, width = 15)
DetectModeOnButton = Button(win, text = "Detection Mode", command = setModeDetect, bg = 'green', height = 2, width = 15)
AutoModeOffButton = Button(win, text = "Autonomous Mode", command = setModeAuto, bg = 'orange', height = 2, width = 15)
AutoModeOnButton = Button(win, text = "Autonomous Mode", command = setModeAuto, bg = 'green', height = 2, width = 15)
OffModeButton = Button(win, text = "System Off", command = setModeOff, bg = 'red', height = 2, width = 15)

setModeOff()

win.protocol("WM_DELETE_WINDOW", close)

win.mainloop()
