import random
import neopixel
from machine import Pin
import time


# Set pins
GoButton = Pin(7, mode=Pin.IN, pull=Pin.PULL_UP)
React1Button = Pin(8, mode=Pin.IN, pull=Pin.PULL_UP) 
React2Button = Pin(9, mode=Pin.IN, pull=Pin.PULL_UP)

GoLight = Pin(25, Pin.OUT)
React1Light = Pin(4, Pin.OUT)
React2Light = Pin(5, Pin.OUT)
RedLight = Pin(12, Pin.OUT)
AmberLight = Pin(13, Pin.OUT)
GreenLight = Pin(14, Pin.OUT)

# Set up the LED strips

LED_num = 40
    #Assume for now same number of LEDs on strips 1 and 2. 

Strip1 = neopixel.NeoPixel(Pin(3), LED_num)
Strip2 = neopixel.NeoPixel(Pin(2), LED_num)

BRIGHTNESS = 1.0

reaction_time = 1  #Typical reaction time for an 85 year old is 1s
game_time = 5
celebration_time = 10

# Definitions

# Light definitions

def set_brightness(color):
    r, g, b = color
    r = int(r * BRIGHTNESS)
    g = int(g * BRIGHTNESS)
    b = int(b * BRIGHTNESS)
    return (r, g, b)
    



def Flash(Strip):
    i=0
    while i < (celebration_time)/3 and GameInProgress == True:

#        if not GoButton.value():
#            time.sleep(0.2)
#            GameInProgress = False

        if Strip == Strip1:
            k=j1
        elif Strip == Strip2:
            k=j2
            #Display red Strip 1
        for l in range(k+1,LED_num):
            color = (255, 0, 0)  
            color = set_brightness(color)
            Strip[l]=(color)
            Strip.write()
        time.sleep(0.5)
        
            # Display green Strip 1
        for l in range(k+1,LED_num):    
            color = (0, 255, 0) 
            color = set_brightness(color)
            Strip[l]=(color)
            Strip.write()
        time.sleep(0.5)

            # Display blue Strip 1
        for l in range(k+1,LED_num):
            color = (0, 0, 255) 
            color = set_brightness(color)
            Strip[l]=(color)
            Strip.write()
        time.sleep(0.5)
                
        i=i+1
        print (i)
        
GameInProgress = True
j1 = 4
j2 = 4



Flash(Strip1)
Flash(Strip2)
