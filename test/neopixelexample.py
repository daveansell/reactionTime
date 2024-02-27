import neopixel
from machine import Pin
import time

ws_pin = 0
led_num = 8
BRIGHTNESS = 0.2  # Adjust the brightness (0.0 - 1.0)

neoRing = neopixel.NeoPixel(Pin(ws_pin), led_num)

def set_brightness(color):
    r, g, b = color
    r = int(r * BRIGHTNESS)
    g = int(g * BRIGHTNESS)
    b = int(b * BRIGHTNESS)
    return (r, g, b)

def loop():
    # Display red
    color = (255, 0, 0)  # Red color
    color = set_brightness(color)
    neoRing.fill(color)
    neoRing.write()
    time.sleep(1)

    # Display green
    color = (0, 255, 0)  # Green color
    color = set_brightness(color)
    neoRing.fill(color)
    neoRing.write()
    time.sleep(1)

    # Display blue
    color = (0, 0, 255)  # Blue color
    color = set_brightness(color)
    neoRing.fill(color)
    neoRing.write()
    time.sleep(1)

while True:
    loop()