import neopixel
from machine import Pin
import time


LED_num = 10
    #Assume for now same number of LEDs on strips 1 and 2. 

Strip1 = neopixel.NeoPixel(Pin(2), LED_num)
Strip2 = neopixel.NeoPixel(Pin(3), LED_num)

BRIGHTNESS = 1.0

def set_brightness(color):
    r, g, b = color
    r = int(r * BRIGHTNESS)
    g = int(g * BRIGHTNESS)
    b = int(b * BRIGHTNESS)
    return (r, g, b)
    
        
def StripsOff(Strip):
    
    # Display red
    color = (0, 0, 0)  # Red color
    color = set_brightness(color)
    Strip.fill(color)
    Strip.write()
        
reaction_time = 2

React1Waiting = True
React2Waiting = True

def RisingLights(Strip):
    print ('i=')
    print (i)
    for j in range(i):
        brightness = int(j/(255/(i+1)))
        #if React1Waiting == True:
        Strip1[j]=(0,brightness,0)
        #if React2Waiting == True:
        Strip2[j]=(0,brightness,0)
        Strip.write

def TooSoon(Strip):
    
    # Display red
    color = (255, 0, 0)  # Red color
    color = set_brightness(color)
    Strip.fill(color)
    Strip.write()


TooSoon(Strip1)
time.sleep(5)
brightness = 0
        #if React1Waiting == True:
Strip1[0]=(0,brightness,0)
Strip1.write()


for i in range (10):
    RisingLights(Strip1)
    time.sleep(reaction_time/2)


