# Libraries

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

LED_num = 70
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
    

def TooSoon(Strip):
    
    # Display red
    color = (255, 0, 0)  # Red color
    color = set_brightness(color)
    Strip.fill(color)
    Strip.write()

def RisingLights():
    global j1
    global j2
    
    if TooSoon1 == True:
        j1 = LED_num
    if TooSoon2 == True:
        j2 = LED_num
    
    for j in range (0,i):
        if React1Waiting == True and TooSoon1 == False:
            brightness = int(j*255/(i*LED_num))
            Strip1[j]=(0,brightness,0)
            Strip1.write()
            j1 = j
        if React2Waiting == True and TooSoon2 == False:
            brightness = int(j*255/(i*LED_num))
            Strip2[j]=(0,brightness,0)
            Strip2.write()
            j2 = j
        
def Flash(Strip):
    

    if Strip == Strip1:
        k=j1
    elif Strip == Strip2:
        k=j2
            
            #Display red Strip 1
    for l in range(k,LED_num):
        color = (255, 0, 0)  
        color = set_brightness(color)
        Strip[l]=(color)
        Strip.write()
    time.sleep(0.5)
        
            # Display green Strip 1
    for l in range(k,LED_num):    
        color = (0, 255, 0) 
        color = set_brightness(color)
        Strip[l]=(color)
        Strip.write()
    time.sleep(0.5)

            # Display blue Strip 1
    for l in range(k,LED_num):
        color = (0, 0, 255) 
        color = set_brightness(color)
        Strip[l]=(color)
        Strip.write()
    time.sleep(0.5)
        
        
    
def StripsOff(Strip):
    
    # Display red
    color = (0, 0, 0)  # Red color
    color = set_brightness(color)
    Strip.fill(color)
    Strip.write()
        
def StopTimer(Strip):
    if (Strip == Strip1):
        Strip1Time = time.ticks_ms()
        React1Light.value(0)
    if (Strip == Strip2):
        Strip2Time = time.ticks_ms()
        React2Light.value(0)
        
#def GoButtonDelay():
#    global GoButton
#    GoButton.value(0)
#    print ('Go button = ')
#    print(GoButton.value)

#    if GoButton == 0:
#        if not GoButton.value():
#            time.sleep(0.2)
#            GoButton = 1
            
    
    
        
def PreGame_sequence():
#    print ('PreGame_sequence')
    
    PreGame_time = True
    
    global TooSoon1
    global TooSoon2
    global GameInProgress
    
    TooSoon1 = False
    TooSoon2 = False
    
    GoLight.value(0)
    RedLight.value(1)
    
    waiting_start = time.ticks_ms()
    random_wait = random.randint(3000, 7000)
    
    while PreGame_time == True and GameInProgress == True:

        if not GoButton.value():
            time.sleep(0.2)
            GameInProgress = False
#            print ('StartButton')

        while time.ticks_ms() - waiting_start < game_time * 1000 and GameInProgress == True:
            

            if not GoButton.value():
                time.sleep(0.2)
                GameInProgress = False
#                print ('StartButton')
            
            if not React1Button.value(): # if the value changes
                TooSoon(Strip1)
                TooSoon1 = True
                #print ('TooSoon Strip1')
                    
            if not React2Button.value(): # if the value changes
                TooSoon(Strip2)
                TooSoon2 = True
                #print ('TooSoon Strip2')
        
        RedLight.value(1)
        AmberLight.value(1)
    
    
    
        while time.ticks_ms() - waiting_start < game_time * 1000 + random_wait and GameInProgress == True:
            
            if not GoButton.value():
                time.sleep(0.2)
                GameInProgress = False
#                print ('StartButton')

            if not React1Button.value(): # if the value changes
                TooSoon(Strip1)
                TooSoon1 = True
            
            if not React2Button.value(): # if the value changes
                TooSoon(Strip2)
                TooSoon2 = True
        
        
        if time.ticks_ms() - waiting_start > game_time * 1000 + random_wait:
            
            RedLight.value(0)
            AmberLight.value(0)
            GreenLight.value(1)
        
            React1Light.value(1)
            React2Light.value(1)
            
            PreGame_time = False

def Game_sequence():

#    print ('Game sequence')

    ReactWaiting = True
    
    global React1Waiting
    global React2Waiting
    
    global Strip1Time
    global Strip2Time
    
    global GameInProgress
    
    React1Waiting = True
    React2Waiting = True

    next_LED_time = reaction_time/LED_num/1000
    
    start = time.ticks_ms() #Records the current time
    
    
    while(ReactWaiting) and GameInProgress == True:
        if not GoButton.value():
            time.sleep(0.2)
            GameInProgress = False
#            print ('StartButton')
        global i
        i=1
        for i in range(LED_num+1): 
            if not React1Button.value():
                Strip1Time = time.ticks_ms()
                React1Waiting = False
            if not React2Button.value():
                Strip2Time = time.ticks_ms()
                React2Waiting = False
            RisingLights()
            time.sleep(next_LED_time)
        ReactWaiting = False

    if TooSoon1 == True:
        Strip1Time = time.ticks_ms()
    
    if TooSoon2 == True:
        Strip2Time = time.ticks_ms()

    if React1Waiting == True:
        Strip1Time = time.ticks_ms()
    
    if React2Waiting == True:
        Strip2Time = time.ticks_ms()
            

    finish_time = time.ticks_ms()
    GreenLight.value(0)

#    print ('End of game time')

def Celebration_sequence():
#    print ('celebration')
    global GameInProgress
    Celebrating = True
    while Celebrating == True and GameInProgress == True:
        global i
        FlashCounter = 0
        if not GoButton.value():
            time.sleep(0.2)
            GameInProgress = False
        if React1Waiting == False and TooSoon1 == False:
#            print ('1Finishes')
            if Strip1Time < Strip2Time:
#                print ('Strip1Faster')
                while FlashCounter < celebration_time/3:
                    Flash(Strip1)
                    FlashCounter = FlashCounter + 1
                StripsOff(Strip1)
                StripsOff(Strip2)
                Celebrating = False
                GameInProgress = False
            elif Strip1Time == Strip2Time:
#                print ('EqualTimes')
                while FlashCounter < celebration_time/3:
                    Flash(Strip1)
                    Flash(Strip2)
                    FlashCounter = FlashCounter + 1
                StripsOff(Strip1)
                StripsOff(Strip2)
                Celebrating = False
                GameInProgress = False
            elif Strip1Time>Strip2Time:
#                print ('Strip1Faster')
                while FlashCounter < celebration_time/3:
                    Flash(Strip2)
                    FlashCounter = FlashCounter + 1
                StripsOff(Strip1)
                StripsOff(Strip2)
                Celebrating = False
                GameInProgress = False
            
        else:
            if React2Waiting == False and TooSoon2 ==False:
#                print ('2Finishes')
                while FlashCounter < celebration_time/3:
                    Flash(Strip2)
                    FlashCounter = FlashCounter + 1
                StripsOff(Strip1)
                StripsOff(Strip2)
                Celebrating = False
                GameInProgress = False
 
        
    

    
    
def StartGame():
#    print ('start')
    PreGame_sequence()
    Game_sequence()
    Celebration_sequence()
    

def Reset():
#    print ('resetting')
    StripsOff(Strip1)
    StripsOff(Strip2)
    GoLight.value(1)
    React1Light.value(0)
    React2Light.value(0)
    RedLight.value(0)
    AmberLight.value(0)
    GreenLight.value(0)
#    print ('reset done')
    
    
# StartGame

GameInProgress = True
Reset()
#LastGoValue = 0
#while TimeToPlay == True:

while GameInProgress == True:
    if not GoButton.value():
        time.sleep(0.2)
        StartGame()
        Reset()
    GameInProgress = True




    
        
        

	






