from machine import Pin
from utime import sleep
from neopixel import NeoPixel

NUMBER_PIXELS = 8
LED_PIN = 22
strip = NeoPixel(Pin(LED_PIN), NUMBER_PIXELS)

strip = NeoPixel(Pin(LED_PIN), NUMBER_PIXELS)

delay = .005

while True:
    for i in range(0, 255):
        strip[0] = (i,0,0) # red=255, green and blue are 0
        strip.write() # send the data from RAM down the wire
        sleep(delay)
    for i in range(255, 0, -1):
        strip[0] = (i,0,0)
        strip.write()
        sleep(delay)