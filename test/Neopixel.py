import neopixel  # Import the neopixel module for controlling the WS2812 LEDs
from machine import Pin  # Import the Pin module for GPIO control
import time  # Import the time module for delays

ws_pin = 0  # GPIO pin connected to the data line of the WS2812 ring
led_num = 8  # Number of LEDs in the WS2812 ring

position = 0  # Variable to keep track of the current position in the rainbow animation
brightness = 0.5  # Adjust the initial brightness (0.0 to 1.0)

neoRing = neopixel.NeoPixel(Pin(ws_pin), led_num)  # Create an instance of the NeoPixel class to control the WS2812 ring

def wheel(pos):
    # Function to generate a color based on a position in the rainbow
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)  # Generate a red-yellow color
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)  # Generate a yellow-green color
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)  # Generate a green-blue color

def loop():
    global position, brightness  # Use global variables for position and brightness

    for i in range(led_num):
        # Iterate through each LED in the ring
        hue = int(i * (255 / led_num) + position) % 256  # Calculate the hue value based on the LED position and current position
        color = wheel(hue)  # Get the color based on the calculated hue
        color = tuple(int(val * brightness) for val in color)  # Adjust the color brightness
        neoRing[(i + position) % led_num] = color  # Set the color of the corresponding LED

    neoRing.write()  # Update the WS2812 ring with the new colors
    position = (position + 1) % led_num  # Increment the position for the next iteration
    time.sleep_ms(200)  # Delay for a short period to control the animation speed

while True:
    loop()  # Run the loop function continuously to display the rainbow animation
