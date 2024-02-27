import neopixel
from machine import Pin



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
    


StripsOff(Strip1)
StripsOff(Strip2)
