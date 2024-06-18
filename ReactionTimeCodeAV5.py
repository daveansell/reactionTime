# Libraries

import random
import neopixel
from machine import Pin, SPI, UART
import utime as time
#import max7219 
from picozero import Speaker
import _thread
from i2ccomms import *


# Set up the key variables we might want to tune

reaction_time = 1000  # ms #Typical reaction time for an 85 year old is 1s
wait_time = 2000  # ms Length of the ''ready' wait
random_wait_short = 2000 # Shortest time for the 'steady' wait
random_wait_long = 4000 # Longest time for the 'steady' wait

celebration_time = 5000  # ms
flash_time = 0.3 #s

FullResetInterval = 60000 # 3 minutes

ScrollPause = 1 # Must be an int (these are counting loops not a specific time interval)

Language = "Norwegian"

#Define the scrolling message
scrolling_messageSoon = "Too soon"
scrolling_messageSlow = "Too slow"
scrolling_messageVisualWait = "Press the button when the green light shows"
scrolling_messageAudioWait = "Wait for the third beep"
scrolling_messageNewGame = "Test your reaction time"
scrolling_messageNewVisual = "Now try with a visual cue"
scrolling_messageNewAudio = "Now try with an audio cue"
scrolling_messageTryAgain = "Try Again"
        
#    if Language == "Norwegian":
#        scrolling_messageSoon = "For fort"
#        scrolling_messageSlow = "For sakte"
#        scrolling_messageVisualWait = "Trykk på knappen når du får grønt lys"
#        scrolling_messageAudioWait = "Trykk på knappen etter tredje pipet"

        

# LED strips

LED_num = 60
BRIGHTNESS = 1.0

LED_interval = int (reaction_time/LED_num) #ms Calculates the time per LED as the lights rise

# Initially set the j numbers for the holding patterns

jVisual1 = LED_num
jVisual2 = LED_num
jAudio1 = LED_num
jAudio2 = LED_num

# LED matrices (different colour LEDs, might need different brightness)

VisualMatrixBrightness = 10

AudioMatrixBrightness = 10

# Set pins

# Buttons

VisualGoButton = Pin(16, mode=Pin.IN, pull=Pin.PULL_UP)
AudioGoButton = Pin(18,mode=Pin.IN, pull=Pin.PULL_UP)
React1Button = Pin(20, mode=Pin.IN, pull=Pin.PULL_UP) 
React2Button = Pin(22, mode=Pin.IN, pull=Pin.PULL_UP)

# Button lights

VisualGoLight = Pin(17, Pin.OUT)
AudioGoLight = Pin(19, Pin.OUT)
React1Light = Pin(21, Pin.OUT)
React2Light = Pin(26, Pin.OUT)

#resetDisplay0 = Pin(14, Pin.OUT)
#resetDisplay0.value(1)
#resetDisplay1 = Pin(10, Pin.OUT)
#resetDisplay1.value(1)

#Speaker

speaker = Speaker(15)

# Set up the hardware

# Set up the LED strips

StripVisual1 = neopixel.NeoPixel(Pin(0), LED_num) #Visual1
StripVisual2 = neopixel.NeoPixel(Pin(4), LED_num) #Visual2
StripAudio1 = neopixel.NeoPixel(Pin(2), LED_num) #Audio1
StripAudio2 = neopixel.NeoPixel(Pin(3), LED_num) #Audio2


# Definitions

# Light definitions

# Set inital flags etc
GameInProgress = True
PreGame_time = False
VisualGameInProgress = False
AudioGameInProgress = False
GameResetFlagVisual = False
GameResetFlagAudio = False
ReactWaiting = False
Celebrating = False

RedLight = False
AmberLight = False
GreenLight = False

TooSoon1 = False
TooSoon2 = False
TooSlow1 = False
TooSlow2 = False

AudioTime1 = None
AudioTime2 = None
VisualTime1 = None
VisualTime2 = None

React1Waiting = False
React2Waiting = False

Celebrating = False

def set_brightness(color):
    r, g, b = color
    r = int(r * BRIGHTNESS)
    g = int(g * BRIGHTNESS)
    b = int(b * BRIGHTNESS)
    return (r, g, b)
    

def TooSoonLights(Strip):
    # Red fill
    color = (255, 0, 0) 
    color = set_brightness(color)
    Strip.fill(color)
    Strip.write()
    
def TooSlowLights(Strip):
    # Green fill
    if Strip == Visual1: 
        color = (0, 255, 0) 
        color = set_brightness(color)
        Strip.fill(color)
        Strip.write()
        
    if Strip == Visual2:
        color = (0, 255, 0) 
        color = set_brightness(color)
        Strip.fill(color)
        Strip.write()
        
        
    # Blue fill
    elif Strip == Audio1:
        color = (0, 0, 255) 
        color = set_brightness(color)
        Strip.fill(color)
        Strip.write()
        
    elif Strip == Audio2:
        color = (0, 0, 255) 
        color = set_brightness(color)
        Strip.fill(color)
        Strip.write()

        
def RisingLights():
    global jVisual1, jVisual2
    global i
    global React1Waiting, React2Waiting, TooSoon1, TooSoon2

    
    for j in range (0,i):
        
        if React1Waiting == True and TooSoon1 == False:
            StripVisual1[j]=(0,255,0)
            jVisual1 = j
            
        if React2Waiting == True and TooSoon2 == False:
            StripVisual2[j]=(0,255,0)
            jVisual2 = j
            
    StripVisual1.write()
    StripVisual2.write()
    
def Flash(Strip,j): # Takes arguments Visual/AudioStrip1/2 and jVisual/Audio1/2
    
    #Flashes the lights above the reaction strip
       
        
            #Display red Strip 1
    for l in range(j,LED_num):
        color = (255, 0, 0)  
        color = set_brightness(color)
        Strip[l]=(color)
    Strip.write()
    time.sleep(flash_time) #s
        
            # Display green Strip 1
    for l in range(j,LED_num):    
        color = (0, 255, 0) 
        color = set_brightness(color)
        Strip[l]=(color)
    Strip.write()
    time.sleep(flash_time) #s

            # Display blue Strip 1
    for l in range(j,LED_num):
        color = (0, 0, 255) 
        color = set_brightness(color)
        Strip[l]=(color)
    Strip.write()
    time.sleep(flash_time) #s
        
def HoldingLights(Strip,j):
     
    # Turns off all the celebration lights leaving only the reaction strip
    
    global LED_num
       
    #Only LEDs that lit during rising lights sequence (or audio equivalent) stay on

    for l in range(j,LED_num):
        color = (0, 0, 0)  
        color = set_brightness(color)
        Strip[l]=(color)

    Strip.write()

    
def StripsOff(Strip):
    
    # Display red
    color = (0, 0, 0)  # Red color
    color = set_brightness(color)
    Strip.fill(color)
    Strip.write()
    
  



def StopTimer(Strip):
    if (Strip == StripVisual1):
        VisualTime1 = time.ticks_ms() #ms
#        React1Light.value(0)

    if (Strip == StripVisual2):
        VisualTime2 = time.ticks_ms() #ms
#        React2Light.value(0)
    

    if (Strip == StripAudio1):
        AudioTime1 = time.ticks_ms() #ms
#        React1Light.value(0)

    if (Strip == StripVAudio2):
        AudioTime2 = time.ticks_ms() #ms
#        React2Light.value(0)




# Game sections

def VisualPreGame_sequence():

    global PreGame_time
    global wait_time
    global TooSoon1, TooSoon2, TooSlow1, TooSlow2
    global VisualGameInProgress
    global ScrollPause
    global scrolling_messageSoon
    
    PreGame_time = True
    
    TooSoon1 = False
    TooSoon2 = False
    TooSlow1 = False
    TooSlow2 = False
    
    StripsOff(StripVisual1)
    StripsOff(StripVisual2)
    
    
    VisualGoButton.value(0)
    AudioGoButton.value(0)
    React1Light.value(1)
    React2Light.value(1)

    sendText(1, 0, C_GREEN, MODE_SCROLL, scrolling_messageVisualWait, scrollspeed=ScrollPause)
    sendText(2, 0, C_GREEN, MODE_SCROLL, scrolling_messageVisualWait, scrollspeed=ScrollPause)
    sendTraffic(1, 1, C_RED, radius=7)
    sendTraffic(2, 1, C_RED, radius=7)
    
    waiting_start = time.ticks_ms() #ms
    random_wait = random.randint(random_wait_short, random_wait_long) # Set the 'steady' wait for this cycle

    while PreGame_time == True and VisualGameInProgress == True:

        while time.ticks_ms() - waiting_start < wait_time and VisualGameInProgress == True:
            if not VisualGoButton.value():
                VisualGameInProgress = False
                time.sleep(0.4) #s
                
            if not AudioGoButton.value():
                VisualGameInProgress = False
                time.sleep(0.4) #s
                
        
            if not React1Button.value(): # if the value changes
                TooSoonLights(StripVisual1)
                TooSoon1 = True
                React1Light.value(0)
                sendText(1, 0, C_RED, MODE_SCROLL, scrolling_messageSoon, scrollspeed=ScrollPause)
                
            if not React2Button.value(): # if the value changes
                TooSoonLights(StripVisual2)
                TooSoon2 = True
                React2Light.value(0)
                sendText(2, 0, C_RED, MODE_SCROLL, scrolling_messageSoon, scrollspeed=ScrollPause)
                
        sendTraffic(1, 1, C_YELLOW, radius=7)
        sendTraffic(2, 1, C_YELLOW, radius=7)

        while time.ticks_ms() - waiting_start < wait_time + random_wait and VisualGameInProgress == True:
            
            if not VisualGoButton.value():
                time.sleep(0.4)
                VisualGameInProgress = False
            if not AudioGoButton.value():
                time.sleep(0.4) #s
                VisualGameInProgress = False

            if not React1Button.value(): # if the value changes
                TooSoonLights(StripVisual1)
                TooSoon1 = True
                React1Light.value(0)
                sendText(1, 0, C_RED, MODE_SCROLL, scrolling_messageSoon, scrollspeed=ScrollPause)
            
            if not React2Button.value(): # if the value changes
                TooSoonLights(StripVisual2)
                TooSoon2 = True
                React2Light.value(0)
                sendText(2, 0, C_RED, MODE_SCROLL, scrolling_messageSoon, scrollspeed=ScrollPause)
        
        if time.ticks_ms() - waiting_start > wait_time + random_wait:
            sendTraffic(1, 1, C_GREEN, radius=8)
            sendTraffic(2, 1, C_GREEN, radius=8)
             
            PreGame_time = False


def VisualGame_sequence():

    global ReactWaiting
    ReactWaiting = True
    
    global TooSoon1, TooSoon2, TooSlow1, TooSlow2
    global VisualTime1, VisualTime2
    global jVisual1, jVisual2
    global React1Waiting, React2Waiting
    global GameResetFlagVisual
    global ScrollPause
    global scrolling_messageSoon
    jVisual1 = 0
    jVisual2 = 0
    VisualTime1 = None
    VisualTime2 = None
    GameResetFlagVisual = True
    
    if TooSoon1 == False:
        React1Waiting = True
    if TooSoon2 == False:
        React2Waiting = True
    
    global VisualGameInProgress
    
    start_time = time.ticks_ms() #Records the current time
    
    while ReactWaiting == True and VisualGameInProgress == True:

        global i
        i=1
        for i in range (1, LED_num):
            timeout = start_time + i * LED_interval # This sets the time at which the next LED comes on
            
            RisingLights()
        
            while time.ticks_ms() < timeout: # Waiting for the next LED, watching for reactions
                if not React1Button.value():
                    if VisualTime1 == None:
                        VisualTime1 = time.ticks_ms()-start_time
                        React1Waiting = False
                        React1Light.value(0)
                        sendText(1, 1, C_GREEN, MODE_RTEXT, str(VisualTime1), scrollspeed=ScrollPause)
                    
                if not React2Button.value():
                    if VisualTime2 == None:
                        VisualTime2 = time.ticks_ms()-start_time
                        React2Waiting = False
                        React2Light.value(0)
                        sendText(2, 1, C_GREEN, MODE_RTEXT, str(VisualTime2), scrollspeed=ScrollPause)

        ReactWaiting = False


    if React1Waiting == True:
        TooSlow1 = True
        VisualTime1 = None
    
    if React2Waiting == True:
        TooSlow2 = True
        VisualTime2 = None
    

    GreenLight = False

def VisualCelebration_sequence():

    global VisualGameInProgress
    global Celebrating
    global TooSoon1, TooSoon2, TooSlow1, TooSlow2
    global VisualTime1, VisualTime2, AudioTime1, AudioTime2
    global scrolling_messageSlow, scrolling_messageSoon
    global scrolling_messageVisualWait
    global ScrollPause
    
    Celebrating = True
    
    if TooSlow1 == True:
        sendText(1, 0, C_RED, MODE_RTEXT, scrolling_messageSlow, scrollspeed=ScrollPause)
    if TooSoon1 == True:
        sendText(1, 0, C_RED, MODE_RTEXT, scrolling_messageSoon, scrollspeed=ScrollPause)
    if TooSoon1 == False and TooSlow1 == False:
        sendText(1, 0, C_GREEN, MODE_RTEXT, str(VisualTime1), scrollspeed=ScrollPause)
                
    if TooSlow2 == True:
        sendText(2, 0, C_RED, MODE_RTEXT, scrolling_messageSlow, scrollspeed=ScrollPause)
    if TooSoon2 == True:
        sendText(2, 0, C_RED, MODE_RTEXT, scrolling_messageSoon, scrollspeed=ScrollPause)
    if TooSoon2 == False and TooSlow2 == False:
        sendText(2, 0, C_GREEN, MODE_RTEXT, str(VisualTime2), scrollspeed=ScrollPause)
                    
    if AudioTime1 is not None: 
        sendText(1, 0, C_BLUE, MODE_RTEXT, str(AudioTime1), scrollspeed=ScrollPause)
    else:
        sendClear(1, 0)
                
    if AudioTime2 is not None: 
        sendText(2, 0, C_BLUE, MODE_RTEXT, str(AudioTime2), scrollspeed=ScrollPause)
    else:
        sendClear(2, 0)   
               
    while Celebrating == True and VisualGameInProgress == True:
        
        global i
        FlashCounter = 0
            
        if VisualTime1 is not None and VisualTime2 is not None:

            if VisualTime1 < VisualTime2:
                while FlashCounter < celebration_time/3/1000:
                    Flash(StripVisual1,jVisual1)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripVisual1,jVisual1)
                HoldingLights(StripVisual2,jVisual2)
    
            elif VisualTime1 == VisualTime2:
                while FlashCounter < celebration_time/3/1000:
                    Flash(StripVisual1,jVisual1)
                    Flash(StripVisual2,jVisual2)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripVisual1,jVisual1)
                HoldingLights(StripVisual2,jVisual2)

            
                
            elif VisualTime1>VisualTime2:
                while FlashCounter < celebration_time/3/1000:
                    Flash(StripVisual2,jVisual2)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripVisual1,jVisual1)
                HoldingLights(StripVisual2,jVisual2)


            
        elif VisualTime1 is None and VisualTime2 is not None:
                while FlashCounter < celebration_time/3/1000:
                    Flash(StripVisual2,jVisual2)
                    FlashCounter = FlashCounter + 1
                StripsOff(StripVisual1)
                HoldingLights(StripVisual2,jVisual2)


                
        elif VisualTime1 is not None and VisualTime2 is None:
            while FlashCounter < celebration_time/3/1000:
                Flash(StripVisual1,jVisual1)
                FlashCounter = FlashCounter + 1
            HoldingLights(StripVisual1,jVisual1)
            StripsOff(StripVisual2)


                
        else:
            time.sleep(5)
#            while FlashCounter < celebration_time/3/1000:
#                time.sleep(3*flash_time)
#                FlashCounter = FlashCounter + 1
            StripsOff(StripVisual1)
            StripsOff(StripVisual2)


        Celebrating = False
        VisualGameInProgress = False
        Reset()

def AudioPreGame_sequence():
    waiting_start = time.ticks_ms() #ms
    random_wait = random.randint(1000, 3000)
    
    global PreGame_time
    PreGame_time = True
    
    global TooSoon1, TooSoon2, TooSlow1, TooSlow2
    global AudioTime1, AudioTime2
    global AudioGameInProgress
    global scrolling_messageAudioWait
    global ScrollPause
    global scrolling_messageSoon


    
    TooSoon1 = False
    TooSoon2 = False
    TooSlow1 = False
    TooSlow2 = False
    AudioTime1 = None
    AudioTime2 = None
    AudioGameInProgress = True
    
    StripsOff(StripAudio1)
    StripsOff(StripAudio2)

    speaker.play('c4', 0.1) # play the middle c for 0.1 seconds
    print ('Beep1')
    
    VisualGoButton.value(0)
    AudioGoButton.value(0)
    
    sendText(1, 0, C_BLUE, MODE_SCROLL, scrolling_messageAudioWait, scrollspeed=ScrollPause)
    sendText(2, 0, C_BLUE, MODE_SCROLL, scrolling_messageAudioWait, scrollspeed=ScrollPause)
    sendClear(1,1) 
    sendClear(2,1) 


    while PreGame_time == True and AudioGameInProgress == True:

        while time.ticks_ms() - waiting_start < wait_time and AudioGameInProgress == True:

            if not AudioGoButton.value():
                time.sleep(0.4) #s
                AudioGameInProgress = False
            if not VisualGoButton.value():
                time.sleep(0.4) #s
                VisualGameInProgress = False

            if not React1Button.value(): # if the value changes
                React1Light.value(0)
                TooSoonLights(StripAudio1)
                TooSoon1 = True
                sendText(1, 0, C_RED, MODE_SCROLL, scrolling_messageSoon, scrollspeed=ScrollPause)

            if not React2Button.value(): # if the value changes
                React2Light.value(0)
                TooSoonLights(StripAudio2)
                TooSoon2 = True
                sendText(2, 0, C_RED, MODE_SCROLL, scrolling_messageSoon, scrollspeed=ScrollPause)
                


        print ('Beep2')
        speaker.play('c4', 0.1) # play the middle c for 0.1 seconds

    
        while time.ticks_ms() - waiting_start < wait_time + random_wait and AudioGameInProgress == True:
            
            if not AudioGoButton.value():
                time.sleep(0.4) #s
                AudioGameInProgress = False
            if not VisualGoButton.value():
                time.sleep(0.4) #s
                AudioGameInProgress = False


            if not React1Button.value(): # if the value changes
                React2Light.value(0)
                TooSoonLights(StripAudio1)
                TooSoon1 = True
                sendText(1, 0, C_RED, MODE_SCROLL, scrolling_messageSoon, scrollspeed=ScrollPause)
                           
            if not React2Button.value(): # if the value changes
                React1Light.value(0)
                TooSoonLights(StripAudio2)
                TooSoon2 = True
                sendText(2, 0, C_RED, MODE_SCROLL, scrolling_messageSoon, scrollspeed=ScrollPause)

        print ('Beeeeep')
        speaker.play('c4',0.2) # play the middle c for 0.1 seconds       
            
        PreGame_time = False

def AudioGame_sequence():
    global ReactWaiting
    ReactWaiting = True
    
    global TooSoon1, TooSoon2, TooSlow1, TooSlow2
    global AudioTime1, AudioTime2
    global jAudio1, jAudio2
    global React1Waiting, React2Waiting
    global GameResetFlagAudio
    global i
    global ScrollPause
    global scrolling_messageSoon
    jAudio1 = 0
    jAudio2 = 0
    AudioTime1 = None
    AudioTime2 = None
    GameResetFlagAudio = True
    
    if TooSoon1 == False:
        React1Waiting = True
    if TooSoon2 == False:
        React2Waiting = True
    
    global AudioGameInProgress
    
    start_time = time.ticks_ms() #Records the current time


    
    while ReactWaiting == True and AudioGameInProgress == True:
        
        i=1
        for i in range(1, LED_num):
            timeout = start_time + i * LED_interval  # This sets the time at which the next LED comes on
        
            if React1Waiting == True and TooSoon1 == False:
                jAudio1 = i
            
            if React2Waiting == True and TooSoon2 == False:           
                jAudio2 = i
                
            while time.ticks_ms() < timeout:  # Waiting for the next LED, watching for reactions
                if not React1Button.value():
                    if AudioTime1 == None:
                        AudioTime1 = time.ticks_ms()-start_time
                        React1Waiting = False
                        React1Light.value(0)
                        sendText(1, 1, C_BLUE, MODE_RTEXT, str(AudioTime1), scrollspeed=ScrollPause)
                if not React2Button.value():
                    if AudioTime2 == None:
                        AudioTime2 = time.ticks_ms()-start_time
                        React2Waiting = False
                        React2Light.value(0)
                        sendText(2, 1, C_BLUE, MODE_RTEXT, str(AudioTime2), scrollspeed=ScrollPause)
            i=i+1
        ReactWaiting = False
        
        for j in range (0,jAudio1):
            StripAudio1[j]=(0,0,255)
        StripAudio1.write()           
            
        for j in range (0,jAudio2):
            StripAudio2[j]=(0,0,255)
        StripAudio2.write()
        
    
                
                
    if React1Waiting == True:
        TooSlow1 = True
        AudioTime1 = None
    
    if React2Waiting == True:
        TooSlow2 = True
        AudioTime2 = None

    ReactWaiting = False
        

 

def AudioCelebration_sequence():

    global AudioGameInProgress
    global Celebrating
    global ScrollPause
    global scrolling_messageSoon
    global scrolling_messageSlow
    global TooSoon1, TooSoon2, TooSlow1, TooSlow2
    global VisualTime1, VisualTime2, AudioTime1, AudioTime2
    
    Celebrating = True
    
    if TooSoon1 == True:
        sendText(1, 1, C_RED, MODE_SCROLL, scrolling_messageSoon, scrollspeed=ScrollPause)
    if TooSlow1 == True:
        sendText(1, 1, C_RED, MODE_SCROLL, scrolling_messageSlow, scrollspeed=ScrollPause)
    if TooSlow1 == False and TooSoon1 == False:
        sendText(1, 1, C_BLUE, MODE_RTEXT, str(AudioTime1), scrollspeed=ScrollPause)
                
    if TooSoon2 ==True:
        sendText(2, 1, C_RED, MODE_SCROLL, scrolling_messageSoon, scrollspeed=ScrollPause)
    if TooSlow2 == True:
        sendText(2, 1, C_RED, MODE_SCROLL, scrolling_messageSlow, scrollspeed=ScrollPause)
    if TooSlow2 == False and TooSoon2 == False:
        sendText(2, 1, C_BLUE, MODE_RTEXT, str(AudioTime2), scrollspeed=ScrollPause)
            
    if VisualTime1 is not None: 
        sendText(1, 1, C_GREEN, MODE_RTEXT, str(VisualTime1), scrollspeed=ScrollPause)
    else:
        sendClear(1,1)
                
    if VisualTime2 is not None: 
        sendText(2, 1, C_GREEN, MODE_RTEXT, str(VisualTime2), scrollspeed=ScrollPause)
    else:
        sendClear(2,1)

               
    while Celebrating == True and AudioGameInProgress == True:
#        global i
        FlashCounter = 0
        if not AudioGoButton.value():
            time.sleep(0.4) #s
            AudioGameInProgress = False
        if not VisualGoButton.value():
            time.sleep(0.4) #s
            VisualGameInProgress = False
            
        if AudioTime1 is not None and AudioTime2 is not None:

            if AudioTime1 < AudioTime2:
                while FlashCounter < celebration_time/3/1000:
                    Flash(StripAudio1,jAudio1)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripAudio1,jAudio1)
                HoldingLights(StripAudio2,jAudio2)

                
                
            elif AudioTime1 == AudioTime2:
                while FlashCounter < celebration_time/3/1000:
                    Flash(StripAudio1,jAudio1)
                    Flash(StripAudio2,jAudio2)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripAudio1,jAudio1)
                HoldingLights(StripAudio2,jAudio2)

                
                
            elif AudioTime1>AudioTime2:
                while FlashCounter < celebration_time/3/1000:
                    Flash(StripAudio2,jAudio2)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripAudio1,jAudio1)
                HoldingLights(StripAudio2,jAudio2)

                
            
        elif AudioTime1 is None and AudioTime2 is not None:
                while FlashCounter < celebration_time/3/1000:
                    Flash(StripAudio2,jAudio2)
                    FlashCounter = FlashCounter + 1
                StripsOff(StripAudio1)
                HoldingLights(StripAudio2,jAudio2)

                
                
        elif AudioTime1 is not None and AudioTime2 is None:
            while FlashCounter < celebration_time/3/1000:
                Flash(StripAudio1,jAudio1)
                FlashCounter = FlashCounter + 1
            HoldingLights(StripAudio1,jAudio1)
            StripsOff(StripAudio2)

            
                
        else:
            time.sleep(5)
#            while FlashCounter < celebration_time/3/1000:
#                time.sleep(3*flash_time)
#                FlashCounter = FlashCounter + 1
            StripsOff(StripAudio1)
            StripsOff(StripAudio2)

        
        Celebrating = False
        AudioGameInProgress = False
        Reset()
            
    

def StartVisualGame():
  #  resetDisplays()
    print ('Visual Pre Game Sequence')
    VisualPreGame_sequence()
    print ('Visual Game Sequence')
    VisualGame_sequence()
    print ('Visual Celebration Sequence')
    VisualCelebration_sequence()
    
def StartAudioGame():
   # resetDisplays()
    print ('Audio Pre Game Sequence')
    AudioPreGame_sequence()
    print ('Audio Game Sequence')
    AudioGame_sequence()
    print ('Audio Celebration Sequence')
    AudioCelebration_sequence()    

def Reset():
    
    print ('Reset')
    global StripVisual1, StripVisual2, StripAudio1, StripAudio2, jVisual1, jVisual2, jAudio1, jAudio2
    global AudioTime1, AudioTime2, VisualTime1, VisualTime2
    global LastResetTime
    global GameResetFlagVisual, GameResetFlagAudio
    
    HoldingLights(StripVisual1, jVisual1)
    HoldingLights(StripVisual2, jVisual2)
    HoldingLights(StripAudio1, jAudio1)
    HoldingLights(StripAudio2, jAudio2)
    
    if GameResetFlagVisual == True:
        print ('VisualFlagTrue')
        if VisualTime1 is None:
            print ('NoVT1')
            sendText(1, 0, C_WHITE, MODE_SCROLL, scrolling_messageTryAgain, scrollspeed=ScrollPause)
        else:
            print ('VT1=')
            print (VisualTime1)
            sendText(1, 0, C_GREEN, MODE_RTEXT, str(VisualTime1), scrollspeed=ScrollPause)
    
        if VisualTime2 is None:
            print ('NoVT2')
            sendText(2, 0, C_WHITE, MODE_SCROLL, scrolling_messageTryAgain, scrollspeed=ScrollPause)
        else:
            print ('VT2=')
            print (VisualTime2)
            sendText(2, 0, C_GREEN, MODE_RTEXT, str(VisualTime2), scrollspeed=ScrollPause)
    else:
        print ('NewVisual')
        sendText(1, 0, C_GREEN, MODE_SCROLL, str(scrolling_messageNewVisual), scrollspeed=ScrollPause)
        sendText(2, 0, C_GREEN, MODE_SCROLL, str(scrolling_messageNewVisual), scrollspeed=ScrollPause)
    
    GameResetFlagVisual = False    
    
    if GameResetFlagAudio == True:
        if AudioTime1 is None: 
            sendText(1, 1, C_WHITE, MODE_SCROLL, scrolling_messageTryAgain, scrollspeed=ScrollPause)
        else:
            sendText(1, 1, C_BLUE, MODE_RTEXT, str(AudioTime1), scrollspeed=ScrollPause)
    
        if AudioTime2 is None: 
            sendText(2, 1, C_WHITE, MODE_SCROLL, scrolling_messageTryAgain, scrollspeed=ScrollPause)
        else:
            sendText(2, 1, C_BLUE, MODE_RTEXT, str(AudioTime2), scrollspeed=ScrollPause)
                
    else:
        sendText(1, 1, C_BLUE, MODE_SCROLL, str(scrolling_messageNewAudio), scrollspeed=ScrollPause)
        sendText(2, 1, C_BLUE, MODE_SCROLL, str(scrolling_messageNewAudio), scrollspeed=ScrollPause)

    GameResetFlagAudio = False

    React1Light.value(0)
    React2Light.value(0)
    
    LastResetTime = time.ticks_ms()
    

def FullReset():
    print ('Full Reset')
    global StripVisual1, StripVisual2, StripAudio1, StripAudio2
    global LastResetTime
    global GameResetFlagVisual, GameResetFlagAudio
    
    GameResetFlagVisual = False
    GameResetFlagAudio = False

    StripsOff(StripVisual1)
    StripsOff(StripVisual2)
    StripsOff(StripAudio1)
    StripsOff(StripAudio2)

    React1Light.value(0)
    React2Light.value(0)
    
    VisualTime1 = None
    VisualTime2 = None
    AudioTime1 = None
    AudioTime2 = None

    jVisual1 = 0
    jVisual2 = 0
    jAudio1 = 0
    jAudio2 = 0
   # resetDisplays()
    sendText(1, 0, C_WHITE, MODE_SCROLL, scrolling_messageNewGame, scrollspeed=ScrollPause)
    sendText(2, 0, C_WHITE, MODE_SCROLL, scrolling_messageNewGame, scrollspeed=ScrollPause)
    sendClear(1,1)
    sendClear(2,1)

    
    LastResetTime = time.ticks_ms()



FullReset()
print("A")

while True:
    GameInProgress = True

    print("B")

    

    while GameInProgress == True: 
        if not VisualGoButton.value():
            time.sleep(0.4) #s
            VisualGameInProgress = True
            AudioGameInProgress = False
            print ('StartVisualGame')
            StartVisualGame()
            
        if not AudioGoButton.value():
            time.sleep(0.4)
            AudioGameInProgress = True
            VisualGameInProgress = False
            print ('StartAudioGame')
            StartAudioGame()
        
        if time.ticks_ms() - LastResetTime > FullResetInterval:
            FullReset()
            
            
    
    
#    GameInProgress = True



    
