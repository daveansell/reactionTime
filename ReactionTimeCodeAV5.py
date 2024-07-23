# Libraries


import random
import neopixel
from machine import Pin, SPI, UART, PWM
import utime as time
#import max7219 
from picozero import Speaker
import _thread
from i2ccomms import *


# Set up the key variables we might want to tune

reaction_time = 1000  # ms #Typical reaction time for an 85 year old is 1s
wait_time = 3000  # ms Length of the ''ready' wait
random_wait_short = 2000 # Shortest time for the 'steady' wait
random_wait_long = 4000 # Longest time for the 'steady' wait
Language = "English"

celebration_time = 5000  # ms
celebration_no_time_wait = 3000
flash_time = 300 #ms

FullResetInterval = 60000 # 1 minute1

ScrollPause = 1 # Must be an int (these are counting loops not a specific time interval)

DefaultLanguage = "English"
scrolling_messageSoon = "Too soon"
scrolling_messageSlow = "Too slow"
scrolling_messageVisualWait = "Press on green light"
scrolling_messageAudioWait = "Press on third beep"
scrolling_messageNewGame = "Test your reaction time"
scrolling_messageNewVisual = "Now try a visual cue"
scrolling_messageNewAudio = "Now try an audio cue"
scrolling_messageTryAgain = "Try Again"


def SetLanguage():
    
    print ("SetLanguage")
    
    global scrolling_messageSoon
    global scrolling_messageSlow
    global scrolling_messageVisualWait
    global scrolling_messageAudioWait
    global scrolling_messageNewGame
    global scrolling_messageNewVisual
    global scrolling_messageNewAudio
    global scrolling_messageTryAgain


    if Language == "English":
        print ("Changing to English messages")
        scrolling_messageSoon = "Too soon"
        scrolling_messageSlow = "Too slow"
        scrolling_messageVisualWait = "Press on green light"
        scrolling_messageAudioWait = "Press on third beep"
        scrolling_messageNewGame = "Test your reaction time"
        scrolling_messageNewVisual = "Now try a visual cue"
        scrolling_messageNewAudio = "Now try an audio cue"
        scrolling_messageTryAgain = "Try Again"
        
    if Language == "Norwegian":
        print ("Changing to Norwegian messages")
        scrolling_messageSoon = "For fort"
        scrolling_messageSlow = "For sakte"
        scrolling_messageVisualWait = "Trykk på knappen når du får grønt lys"
        scrolling_messageAudioWait = "Trykk på knappen etter tredje pipet"
        scrolling_messageNewGame = "NorwegianNewGameMessage"
        scrolling_messageNewVisual = "NorwegianNewVisualMessage"
        scrolling_messageNewAudio = "NorwegianNewAudioMessage"
        scrolling_messageTryAgain = "NorwegianTryAgainMessage"
        
#Then actually change the currentscreen text...
        
    if VisualTime1 is not None or VisualTime2 is not None:
        if VisualTime1 is None:
            sendText(1, 0, C_GREEN, MODE_SCROLL, scrolling_messageNewVisual, scrollspeed=ScrollPause, size = 1.5)
        else:
            sendText(1, 0, C_GREEN, MODE_RTEXT, str(int(VisualTime1)), scrollspeed=ScrollPause, size = 1.5)
    
        if VisualTime2 is None:
            sendText(2, 0, C_GREEN, MODE_SCROLL, scrolling_messageNewVisual, scrollspeed=ScrollPause, size = 1.5)
        else:
            sendText(2, 0, C_GREEN, MODE_RTEXT, str(int(VisualTime2)), scrollspeed=ScrollPause, size = 1.5)
    else:
        sendText(1, 0, C_WHITE, MODE_SCROLL, str(scrolling_messageNewGame), scrollspeed=ScrollPause, size = 1.5)
        sendText(2, 0, C_WHITE, MODE_SCROLL, str(scrolling_messageNewGame), scrollspeed=ScrollPause, size = 1.5)    
    
    if VisualTime1 is not None or VisualTime2 is not None:
        if AudioTime1 is None: 
            sendText(1, 1, C_BLUE, MODE_SCROLL, scrolling_messageNewAudio, scrollspeed=ScrollPause, size = 1.5)
        else:
            sendText(1, 1, C_BLUE, MODE_RTEXT, str(int(AudioTime1)), scrollspeed=ScrollPause, size = 1.5)
    
        if AudioTime2 is None: 
            sendText(2, 1, C_BLUE, MODE_SCROLL, scrolling_messageNewAudio, scrollspeed=ScrollPause, size = 1.5)
        else:
            sendText(2, 1, C_BLUE, MODE_RTEXT, str(int(AudioTime2)), scrollspeed=ScrollPause, size = 1.5)
                
    else:
        sendText(1, 1, C_BLUE, MODE_SCROLL, str(scrolling_messageNewGame), scrollspeed=ScrollPause, size = 1.5)
        sendText(2, 1, C_BLUE, MODE_SCROLL, str(scrolling_messageNewGame), scrollspeed=ScrollPause, size = 1.5)

        

# LED strips

LED_num = 144
BRIGHTNESS = 1.0

reaction_interval = 25 #ms Calculates the time per LED as the lights rise

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
LanguageButton = Pin(27, mode=Pin.IN, pull=Pin.PULL_UP)

# Button lights

VisualGoLight = Pin(17, Pin.OUT)
AudioGoLight = Pin(19, Pin.OUT)
React1Light = Pin(21, Pin.OUT)
React2Light = Pin(26, Pin.OUT)

#Speaker

#speaker = Speaker(15)

Frequency = 523 #c5
Buzzer = Pin(15)

LongBeep = 200
ShortBeep = 100

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
VisualRestartFlag = False
AudioRestartFlag = False

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

    
    
def Flash(Strip,j): # Takes arguments Visual/AudioStrip1/2 and jVisual/Audio1/2
    
    #Flashes the lights above the reaction strip
        
            #Display red Strip 1
    for l in range(j,LED_num):
        color = (255, 0, 0)  
        color = set_brightness(color)
        Strip[l]=(color)
    Strip.write()
    flash_start = time.ticks_ms()
    while time.ticks_ms() < flash_start + flash_time:
        RestartWatch()
        
            # Display green Strip 1
    for l in range(j,LED_num):    
        color = (0, 255, 0) 
        color = set_brightness(color)
        Strip[l]=(color)
    Strip.write()
    flash_start = time.ticks_ms()
    while time.ticks_ms() < flash_start + flash_time:
        RestartWatch()

            # Display blue Strip 1
    for l in range(j,LED_num):
        color = (0, 0, 255) 
        color = set_brightness(color)
        Strip[l]=(color)
    Strip.write()
    flash_start = time.ticks_ms()
    while time.ticks_ms() < flash_start + flash_time:
        RestartWatch()
        
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


def RestartWatch():
    
    global VisualGameInProgress, AudioGameInProgress
    global VisualRestartFlag, AudioRestartFlag
    global PreGame_time, ReactWaiting, Celebrating
    global TooSoon1, TooSoon2, TooSlow1, TooSlow2
    
    
    if not VisualGoButton.value():
        time.sleep(0.4) #s
        VisualGameInProgress = False
        AudioGameInProgress = False
        PreGame_time = False
        ReactWaiting = False
        Celebrating = False
        TooSlow1 = False
        TooSlow2 = False
        VisualRestartFlag = True
        sendClear(0, 1)
        sendClear(0, 2)
        sendClear(1, 1)
        sendClear(1, 2)
    
            
    if not AudioGoButton.value():
        time.sleep(0.4) #s
        VisualGameInProgress = False
        AudioGameInProgress = False
        PreGame_time = False
        ReactWaiting = False
        Celebrating = False
        TooSoon1 = False
        TooSoon2 = False
        TooSlow1 = False
        TooSlow2 = False
        AudioRestartFlag = True
        sendClear(0, 1)
        sendClear(0, 2)
        sendClear(1, 1)
        sendClear(1, 2)



# Game sections

def VisualPreGame_sequence():
    print ("VisualPreGame_sequence")
    global PreGame_time
    PreGame_time = True
    
    global TooSoon1, TooSoon2, TooSlow1, TooSlow2
    global VisualTime1, VisualTime2
    global VisualGameInProgress
    global ScrollPause, wait_time
    global scrolling_messageSoon, scrolling_messageSlow
    global scrolling_messageVisualWait, scrolling_messageAudioWait
    global scrolling_messageNewGame, scrolling_messageNewVisual, scrolling_messageNewAudio, scrolling_messageTryAgain
    global GameResetFlagVisual, GameResetFlagAudio
    
    TooSoon1 = False
    TooSoon2 = False
    TooSlow1 = False
    TooSlow2 = False
    VisualTime1 = None
    VisualTime2 = None
    VisualGameInProgress = True
    
    
    StripsOff(StripVisual1)
    StripsOff(StripVisual2)
    
    
    VisualGoButton.value(0)
    AudioGoButton.value(0)
    React1Light.value(1)
    React2Light.value(1)

    sendText(1, 0, C_GREEN, MODE_SCROLL, scrolling_messageVisualWait, scrollspeed=ScrollPause, size = 1.5)
    sendText(2, 0, C_GREEN, MODE_SCROLL, scrolling_messageVisualWait, scrollspeed=ScrollPause, size = 1.5)
    sendTraffic(1, 1, C_RED, radius=7)
    sendTraffic(2, 1, C_RED, radius=7)

    
    waiting_start = time.ticks_ms() #ms
    random_wait = random.randint(random_wait_short, random_wait_long) # Set the 'steady' wait for this cycle
        
    
    
    while PreGame_time == True and VisualGameInProgress == True:
        
        RestartWatch() 

        while time.ticks_ms() - waiting_start < wait_time and VisualGameInProgress == True:
            
            RestartWatch()                
        
            if not React1Button.value(): # if the value changes
                React1Light.value(0)
                TooSoonLights(StripVisual1)
                TooSoon1 = True
                sendText(1, 0, C_RED, MODE_SCROLL, scrolling_messageSoon, scrollspeed=ScrollPause, size = 1.5)
                
            if not React2Button.value(): # if the value changes
                React2Light.value(0)
                TooSoonLights(StripVisual2)
                TooSoon2 = True
                sendText(2, 0, C_RED, MODE_SCROLL, scrolling_messageSoon, scrollspeed=ScrollPause, size = 1.5)
                
            if TooSoon1 == True and TooSoon2 == True:
                TooSoonClock = time.ticks_ms()
                while time.ticks_ms() < TooSoonClock + 2000:
                    RestartWatch()
                PreGameTime = False
                VisualGameInProgress = False
                GameResetFlagVisual = True
                Reset()
                
                
                
        sendTraffic(1, 1, C_YELLOW, radius=7)
        sendTraffic(2, 1, C_YELLOW, radius=7)

        while time.ticks_ms() - waiting_start < wait_time + random_wait and VisualGameInProgress == True:
            
            RestartWatch()

            if not React1Button.value(): # if the value changes
                React1Light.value(0)
                TooSoonLights(StripVisual1)
                TooSoon1 = True
                sendText(1, 0, C_RED, MODE_SCROLL, scrolling_messageSoon, scrollspeed=ScrollPause, size = 1.5)
            
            if not React2Button.value(): # if the value changes
                React2Light.value(0)
                TooSoonLights(StripVisual2)
                TooSoon2 = True
                sendText(2, 0, C_RED, MODE_SCROLL, scrolling_messageSoon, scrollspeed=ScrollPause, size = 1.5)
            
            if TooSoon1 == True and TooSoon2 == True:
                TooSoonClock = time.ticks_ms()
                while time.ticks_ms() < TooSoonClock + 2000:
                    RestartWatch()
                PreGameTime = False
                VisualGameInProgress = False
                GameResetFlagVisual = True
                Reset()
        
        sendTraffic(1, 1, C_GREEN, radius=8)
        sendTraffic(2, 1, C_GREEN, radius=8)
             
        PreGame_time = False


def VisualGame_sequence():
    print ("VisualGame_sequence")
    
    global ReactWaiting
    ReactWaiting = True
    
    global TooSoon1, TooSoon2, TooSlow1, TooSlow2
    global VisualTime1, VisualTime2
    global jVisual1, jVisual2
    global React1Waiting, React2Waiting
    global GameResetFlagVisual
    global VisualGameInProgress
    global i, LED_num, reaction_time
    global ScrollPause
    global scrolling_messageSoon, scrolling_messageSlow
    global scrolling_messageVisualWait, messageAudioWait
    global scrolling_messageNewGame, scrolling_messageNewVisual, scrolling_messageNewAudio, scrolling_messageTryAgain

    jVisual1 = 0
    jVisual2 = 0
    VisualTime1 = None
    VisualTime2 = None
    GameResetFlagVisual = True

    
    if VisualGameInProgress == False:
        Reset()
    
    if TooSoon1 == False:
        React1Waiting = True
        
    if TooSoon2 == False:
        React2Waiting = True
    
    start_time = time.ticks_ms() #Records the current time
    
    while ReactWaiting == True and VisualGameInProgress == True:

        i=1
        for i in range (i, int(reaction_time/reaction_interval)):
            
            timeout = start_time + i * reaction_interval

        
            while time.ticks_ms() < timeout: # Waiting for the next LED, watching for reactions

                if not React1Button.value():
                    if VisualTime1 == None:
                        VisualTime1 = time.ticks_ms()-start_time
                        jVisual1 = int(float(LED_num)*float(VisualTime1)/reaction_time)
                        React1Waiting = False
                        React1Light.value(0)
                        sendText(1, 0, C_GREEN, MODE_RTEXT, str(int(VisualTime1)), scrollspeed=ScrollPause, size = 1.5)
                    
                if not React2Button.value():
                    if VisualTime2 == None:
                        VisualTime2 = time.ticks_ms()-start_time
                        jVisual2 = int(float(LED_num)*float(VisualTime2)/reaction_time)
                        React2Waiting = False
                        React2Light.value(0)
                        sendText(2, 0, C_GREEN, MODE_RTEXT, str(int(VisualTime2)), scrollspeed=ScrollPause, size = 1.5)
            
                LED_climb = min(int(LED_num * float(timeout-start_time)/reaction_time),143)      
            
                for j in range (0,LED_climb):
                    if React1Waiting == True and TooSoon1 == False:
                        StripVisual1[j]=(0,255,0)
                        jVisual1 = j
                        
            
                    if React2Waiting == True and TooSoon2 == False:
                        StripVisual2[j]=(0,255,0)
                        jVisual2 = j
                        
                StripVisual1.write()
                StripVisual2.write()
        ReactWaiting = False
        
    for j in range (0, min(143,jVisual1)):
        StripVisual1[j]=(0,255,0)
    
    for j in range (0, min(143,jVisual2)):
        StripVisual2[j]=(0,255,0)

    if React1Waiting == True:
        TooSlow1 = True

        VisualTime1 = None
    
    if React2Waiting == True:
        TooSlow2 = True
        VisualTime2 = None
    
    ReactWaiting = False

def VisualCelebration_sequence():
    print ("VisualCelebration_sequence")

    global VisualGameInProgress
    global Celebrating
    global ScrollPause
    global scrolling_messageSoon, scrolling_messageSlow
    global scrolling_messageVisualWait, scrolling_messageAudioWait
    global scrolling_messageNewGame, scrolling_messageNewVisual, scrolling_messageNewAudio, scrolling_messageTryAgain
    global celebration_no_time_wait
    global TooSoon1, TooSoon2, TooSlow1, TooSlow2
    global VisualTime1, VisualTime2, AudioTime1, AudioTime2
    global jVisual1, jVisual2
    
    if VisualGameInProgress == False:
        Reset()
    
    Celebrating = True
    
    if Celebrating == True and TooSlow1 == True:
        sendText(1, 0, C_RED, MODE_SCROLL, scrolling_messageSlow, scrollspeed=ScrollPause, size = 1.5)
    if Celebrating == True and TooSoon1 == True:
        sendText(1, 0, C_RED, MODE_SCROLL, scrolling_messageSoon, scrollspeed=ScrollPause, size = 1.5)
    if Celebrating == True and TooSoon1 == False and TooSlow1 == False:
        sendText(1, 0, C_GREEN, MODE_RTEXT, str(int(VisualTime1)), scrollspeed=ScrollPause, size = 1.5)
                
    if Celebrating == True and TooSlow2 == True:
        sendText(2, 0, C_RED, MODE_SCROLL, scrolling_messageSlow, scrollspeed=ScrollPause, size = 1.5)
    if Celebrating == True and TooSoon2 == True:
        sendText(2, 0, C_RED, MODE_SCROLL, scrolling_messageSoon, scrollspeed=ScrollPause, size = 1.5)
    if Celebrating == True and TooSoon2 == False and TooSlow2 == False:
        sendText(2, 0, C_GREEN, MODE_RTEXT, str(int(VisualTime2)), scrollspeed=ScrollPause, size = 1.5)
                    
    if Celebrating == True and AudioTime1 is not None: 
        sendText(1, 1, C_BLUE, MODE_RTEXT, str(int(AudioTime1)), scrollspeed=ScrollPause, size = 1.5)
    else:
        sendClear(1, 1)
                
    if Celebrating == True and AudioTime2 is not None: 
        sendText(2, 1, C_BLUE, MODE_RTEXT, str(int(AudioTime2)), scrollspeed=ScrollPause, size = 1.5)
    else:
        sendClear(2, 1)   
               
    while Celebrating == True and VisualGameInProgress == True:
        
        RestartWatch()
        
        global i
        FlashCounter = 0
            
        if VisualTime1 is not None and VisualTime2 is not None:

            if VisualTime1 < VisualTime2:
                while FlashCounter < (celebration_time/flash_time)/3 and VisualGameInProgress == True:
                    RestartWatch()
                    Flash(StripVisual1,jVisual1)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripVisual1,jVisual1)
                HoldingLights(StripVisual2,jVisual2)
    
            elif VisualTime1 == VisualTime2:
                while FlashCounter < (celebration_time/flash_time)/3 and VisualGameInProgress == True:
                    RestartWatch()
                    Flash(StripVisual1,jVisual1)
                    Flash(StripVisual2,jVisual2)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripVisual1,jVisual1)
                HoldingLights(StripVisual2,jVisual2)

            
                
            elif VisualTime1>VisualTime2:
                while FlashCounter < (celebration_time/flash_time)/3 and VisualGameInProgress == True:
                    RestartWatch()
                    Flash(StripVisual2,jVisual2)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripVisual1,jVisual1)
                HoldingLights(StripVisual2,jVisual2)


            
        elif VisualTime1 is None and VisualTime2 is not None:
                while FlashCounter < (celebration_time/flash_time)/3 and VisualGameInProgress == True:
                    RestartWatch()
                    Flash(StripVisual2,jVisual2)
                    FlashCounter = FlashCounter + 1
                StripsOff(StripVisual1)
                HoldingLights(StripVisual2,jVisual2)


                
        elif VisualTime1 is not None and VisualTime2 is None:
            while FlashCounter < (celebration_time/flash_time)/3 and VisualGameInProgress == True:
                RestartWatch()
                Flash(StripVisual1,jVisual1)
                FlashCounter = FlashCounter + 1
            HoldingLights(StripVisual1,jVisual1)
            StripsOff(StripVisual2)


                
        else:
            NoCelebrationTime = time.ticks_ms()
            
            while time.ticks_ms() < NoCelebrationTime + celebration_no_time_wait and VisualGameInProgress == True:
                RestartWatch()
            StripsOff(StripVisual1)
            StripsOff(StripVisual2)


        Celebrating = False
        VisualGameInProgress = False
        Reset()

def AudioPreGame_sequence():
    print ("AudioPreGame_sequence")
    global PreGame_time
    PreGame_time = True
    
    global TooSoon1, TooSoon2, TooSlow1, TooSlow2
    global AudioTime1, AudioTime2
    global AudioGameInProgress
    global scrolling_messageSoon, scrolling_messageSlow
    global scrolling_messageVisualWait, scrolling_messageAudioWait
    global scrolling_messageNewGame, scrolling_messageNewVisual, scrolling_messageNewAudio, G
    
    TooSoon1 = False
    TooSoon2 = False
    TooSlow1 = False
    TooSlow2 = False
    AudioTime1 = None
    AudioTime2 = None
    AudioGameInProgress = True
    

    StripsOff(StripAudio1)
    StripsOff(StripAudio2)
    
    VisualGoButton.value(0)
    AudioGoButton.value(0)
    
    sendText(1, 0, C_BLUE, MODE_SCROLL, scrolling_messageAudioWait, scrollspeed=ScrollPause, size = 1.5)
    sendText(2, 0, C_BLUE, MODE_SCROLL, scrolling_messageAudioWait, scrollspeed=ScrollPause, size = 1.5)

    sendClear(1,1) 
    sendClear(2,1)

    
    waiting_start = time.ticks_ms() #ms
    random_wait = random.randint(1000, 3000)
 
 
    
    while PreGame_time == True and AudioGameInProgress == True:
        
        RestartWatch()   
    
        BeepOnTime = time.ticks_ms()
        
        Beep = PWM(Buzzer)
        Beep.freq(Frequency) #c5
        Beep.duty_u16(32768) #50% 
        
        while time.ticks_ms() < BeepOnTime+ShortBeep:
              
            RestartWatch()

            if not React1Button.value(): # if the value changes
                React1Light.value(0)
                TooSoonLights(StripAudio1)
                TooSoon1 = True
                sendText(1, 0, C_RED, MODE_SCROLL, scrolling_messageSoon, scrollspeed=ScrollPause, size = 1.5)

            if not React2Button.value(): # if the value changes
                React2Light.value(0)
                TooSoonLights(StripAudio2)
                TooSoon2 = True
                sendText(2, 0, C_RED, MODE_SCROLL, scrolling_messageSoon, scrollspeed=ScrollPause, size = 1.5)
            
            if TooSoon1 == True and TooSoon2 == True:
                TooSoonClock = time.ticks_ms()
                while time.ticks_ms() < TooSoonClock + 2000:
                    RestartWatch()
                PreGameTime = False
                AudioGameInProgress = False
                GameResetFlagAudio = True
                Reset()

        Beep.deinit()
    
    

        while time.ticks_ms() - waiting_start < wait_time and AudioGameInProgress == True:

            RestartWatch()

            if not React1Button.value(): # if the value changes
                React1Light.value(0)
                TooSoonLights(StripAudio1)
                TooSoon1 = True
                sendText(1, 0, C_RED, MODE_SCROLL, scrolling_messageSoon, scrollspeed=ScrollPause, size = 1.5)

            if not React2Button.value(): # if the value changes
                React2Light.value(0)
                TooSoonLights(StripAudio2)
                TooSoon2 = True
                sendText(2, 0, C_RED, MODE_SCROLL, scrolling_messageSoon, scrollspeed=ScrollPause, size = 1.5)
                
            if TooSoon1 == True and TooSoon2 == True:
                TooSoonClock = time.ticks_ms()
                while time.ticks_ms() < TooSoonClock + 2000:
                    RestartWatch()
                PreGameTime = False
                AudioGameInProgress = False
                GameResetFlagAudio = True
                Reset()
                
        BeepOnTime = time.ticks_ms()
        
        Beep = PWM(Buzzer)
        Beep.freq(Frequency) #c5
        Beep.duty_u16(32768) #50%   
        
        while time.ticks_ms() < BeepOnTime+ShortBeep:
            
            RestartWatch()

            if not React1Button.value(): # if the value changes
                React1Light.value(0)
                TooSoonLights(StripAudio1)
                TooSoon1 = True
                sendText(1, 0, C_RED, MODE_SCROLL, scrolling_messageSoon, scrollspeed=ScrollPause, size = 1.5)

            if not React2Button.value(): # if the value changes
                React2Light.value(0)
                TooSoonLights(StripAudio2)
                TooSoon2 = True
                sendText(2, 0, C_RED, MODE_SCROLL, scrolling_messageSoon, scrollspeed=ScrollPause, size = 1.5)
                
            if TooSoon1 == True and TooSoon2 == True:
                TooSoonClock = time.ticks_ms()
                while time.ticks_ms() < TooSoonClock + 2000:
                    RestartWatch()
                PreGameTime = False
                VisualGameInProgress = False
                AudioGameInProgress = False
                GameResetFlagAudio = True
                Reset()

        Beep.deinit()        
                
                
        while time.ticks_ms() - waiting_start < wait_time + random_wait and AudioGameInProgress == True:
            
            RestartWatch()


            if not React1Button.value(): # if the value changes
                React1Light.value(0)
                TooSoonLights(StripAudio1)
                TooSoon1 = True
                sendText(1, 0, C_RED, MODE_SCROLL, scrolling_messageSoon, scrollspeed=ScrollPause, size = 1.5)
                           
            if not React2Button.value(): # if the value changes
                React2Light.value(0)
                TooSoonLights(StripAudio2)
                TooSoon2 = True
                sendText(2, 0, C_RED, MODE_SCROLL, scrolling_messageSoon, scrollspeed=ScrollPause, size = 1.5)
                
            if TooSoon1 == True and TooSoon2 == True:
                TooSoonClock = time.ticks_ms()
                while time.ticks_ms() < TooSoonClock + 2000:
                    RestartWatch()
                PreGameTime = False
                VisualGameInProgress = False
                AudioGameInProgress = False
                GameResetFlagAudio = True
                Reset()

                
        PreGame_time = False

def AudioGame_sequence():
    print ("AudioGame_sequence")
    
    global ReactWaiting
    ReactWaiting = True
    
    global AudioGameInProgress
    global TooSoon1, TooSoon2, TooSlow1, TooSlow2
    global AudioTime1, AudioTime2
    global jAudio1, jAudio2
    global React1Waiting, React2Waiting
    global GameResetFlagAudio
    global i
    global ScrollPause
    global scrolling_messageSoon, scrolling_messageSlow
    global scrolling_messageVisualWait, scrolling_messageAudioWait
    global scrolling_messageNewGame, scrolling_messageNewVisual, scrolling_messageNewAudio
    scrolling_messageTryAgain
    global LED_num, reaction_time
    jAudio1 = 0
    jAudio2 = 0
    AudioTime1 = None
    AudioTime2 = None
    GameResetFlagAudio = True
    
    if AudioGameInProgress == False:
        Reset()
    
    if TooSoon1 == False:
        React1Waiting = True
    if TooSoon2 == False:
        React2Waiting = True
    
    
    
    
    start_time = time.ticks_ms() #Records the current time


    while ReactWaiting == True and AudioGameInProgress == True:
        
        Beep = PWM(Buzzer)
        Beep.freq(Frequency) #c5
        Beep.duty_u16(32768) #50%
        
        while time.ticks_ms() < start_time + LongBeep:

            if not React1Button.value():
                if AudioTime1 == None:
                    AudioTime1 = time.ticks_ms()-start_time
                    jAudio1 = int(float(LED_num)*float(AudioTime1)/reaction_time)
                    React1Waiting = False
                    React1Light.value(0)
                    sendText(1, 1, C_BLUE, MODE_RTEXT, str(int(AudioTime1)), scrollspeed=ScrollPause, size = 1.5)
                
            if not React2Button.value():
                if AudioTime2 == None:
                    AudioTime2 = time.ticks_ms()-start_time
                    jAudio2 = int(float(LED_num)*float(AudioTime2)/reaction_time)
                    React2Waiting = False
                    React2Light.value(0)
                    sendText(2, 1, C_BLUE, MODE_RTEXT, str(int(AudioTime2)), scrollspeed=ScrollPause, size = 1.5)

                    
        
        Beep.deinit()


        timeout = start_time + reaction_time  # This sets the time at which the next LED comes on
                        
        while time.ticks_ms() < timeout:  # Waiting for the next LED, watching for reactions
                if not React1Button.value():
                    if AudioTime1 == None:
                        AudioTime1 = time.ticks_ms()-start_time
                        jAudio1 = int(float(LED_num)*float(AudioTime1)/reaction_time)
                        React1Waiting = False
                        React1Light.value(0)
                        sendText(1, 1, C_BLUE, MODE_RTEXT, str(int(AudioTime1)), scrollspeed=ScrollPause, size = 1.5)
                
                if not React2Button.value():
                    if AudioTime2 == None:
                        AudioTime2 = time.ticks_ms()-start_time
                        jAudio2 = int(float(LED_num)*float(AudioTime2)/reaction_time)
                        React2Waiting = False
                        React2Light.value(0)
                        sendText(2, 1, C_BLUE, MODE_RTEXT, str(int(AudioTime2)), scrollspeed=ScrollPause, size = 1.5)

                                
        ReactWaiting = False
        
        
        for j in range (0, min(143,jAudio1)):
            StripAudio1[j]=(0,0,255)           
            
        for j in range (0,min(143,jAudio2)):
            StripAudio2[j]=(0,0,255)
        
        StripAudio1.write()
        StripAudio2.write()
                        
    if React1Waiting == True:
        TooSlow1 = True
        AudioTime1 = None
    
    if React2Waiting == True:
        TooSlow2 = True
        AudioTime2 = None

    ReactWaiting = False
        

 

def AudioCelebration_sequence():
    print ("AudioCelebration_sequence")

    global AudioGameInProgress
    global Celebrating
    global ScrollPause
    global celebration_no_time_wait
    global scrolling_messageSoon, scrolling_messageSlow
    global scrolling_messageVisualWait, scrolling_messageAudioWait
    global scrolling_messageNewGame, scrolling_messageNewVisual, scrolling_messageNewAudio, scrolling_messageTryAgain
    global TooSoon1, TooSoon2, TooSlow1, TooSlow2
    global VisualTime1, VisualTime2, AudioTime1, AudioTime2
    
    if AudioGameInProgress == False:
        Reset()
    
    Celebrating = True
    
    if TooSoon1 == True:
        sendText(1, 1, C_RED, MODE_SCROLL, scrolling_messageSoon, scrollspeed=ScrollPause, size = 1.5)
    if TooSlow1 == True:
        sendText(1, 1, C_RED, MODE_SCROLL, scrolling_messageSlow, scrollspeed=ScrollPause, size = 1.5)
    if TooSlow1 == False and TooSoon1 == False:
        sendText(1, 1, C_BLUE, MODE_RTEXT, str(int(AudioTime1)), scrollspeed=ScrollPause, size = 1.5)
                
    if TooSoon2 ==True:
        sendText(2, 1, C_RED, MODE_SCROLL, scrolling_messageSoon, scrollspeed=ScrollPause, size = 1.5)
    if TooSlow2 == True:
        sendText(2, 1, C_RED, MODE_SCROLL, scrolling_messageSlow, scrollspeed=ScrollPause, size = 1.5)
    if TooSlow2 == False and TooSoon2 == False:
        sendText(2, 1, C_BLUE, MODE_RTEXT, str(int(AudioTime2)), scrollspeed=ScrollPause, size = 1.5)
            
    if VisualTime1 is not None: 
        sendText(1, 0, C_GREEN, MODE_RTEXT, str(int(VisualTime1)), scrollspeed=ScrollPause, size = 1.5)
    else:
        sendClear(1,0)
                
    if VisualTime2 is not None: 
        sendText(2, 0, C_GREEN, MODE_RTEXT, str(int(VisualTime2)), scrollspeed=ScrollPause, size = 1.5)
    else:
        sendClear(2,0)

               
    while Celebrating == True and AudioGameInProgress == True:
#
        RestartWatch()
        FlashCounter = 0
        
        if AudioTime1 is not None and AudioTime2 is not None:

            if AudioTime1 < AudioTime2:
                while FlashCounter < (celebration_time/flash_time)/3 and AudioGameInProgress == True:
                    RestartWatch()
                    Flash(StripAudio1,jAudio1)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripAudio1,jAudio1)
                HoldingLights(StripAudio2,jAudio2)

            elif AudioTime1 == AudioTime2:
                while FlashCounter < (celebration_time/flash_time)/3 and AudioGameInProgress == True:
                    RestartWatch()
                    Flash(StripAudio1,jAudio1)
                    Flash(StripAudio2,jAudio2)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripAudio1,jAudio1)
                HoldingLights(StripAudio2,jAudio2)

                
                
            elif AudioTime1>AudioTime2:
                while FlashCounter < (celebration_time/flash_time)/3 and AudioGameInProgress == True:
                    RestartWatch()
                    Flash(StripAudio2,jAudio2)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripAudio1,jAudio1)
                HoldingLights(StripAudio2,jAudio2)

                
            
        elif AudioTime1 is None and AudioTime2 is not None:
                while FlashCounter < (celebration_time/flash_time)/3 and AudioGameInProgress == True:
                    RestartWatch()
                    Flash(StripAudio2,jAudio2)
                    FlashCounter = FlashCounter + 1
                StripsOff(StripAudio1)
                HoldingLights(StripAudio2,jAudio2)

                
                
        elif AudioTime1 is not None and AudioTime2 is None:
            while FlashCounter < (celebration_time/flash_time)/3 and AudioGameInProgress == True:
                RestartWatch()
                Flash(StripAudio1,jAudio1)
                FlashCounter = FlashCounter + 1
            HoldingLights(StripAudio1,jAudio1)
            StripsOff(StripAudio2)

            
                
        else:
            NoCelebrationTime = time.ticks_ms()
            
            while time.ticks_ms() < NoCelebrationTime + celebration_no_time_wait and AudioGameInProgress == True:
                RestartWatch()
                
            StripsOff(StripAudio1)
            StripsOff(StripAudio2)

        
        Celebrating = False
        AudioGameInProgress = False
        Reset()
            
    

def StartVisualGame():
    global VisualRestartFlag, AudioRestartFlag
    global VisualGameInProgress
    
    VisualRestartFlag = False
    
    print ("StartVisualGame")
    
    if VisualGameInProgress == True:        
        VisualPreGame_sequence()
    if VisualGameInProgress == True:
        VisualGame_sequence()
    if VisualGameInProgress == True:
        VisualCelebration_sequence()
    
def StartAudioGame():
    global VisualRestartFlag, AudioRestartFlag
    global AudioGameInProgress
    
    AudioRestartFlag = False
    
    print ("StartAudioGame")
    
    if AudioGameInProgress == True:
        AudioPreGame_sequence()
    if AudioGameInProgress == True:        
        AudioGame_sequence()
    if AudioGameInProgress == True:
        AudioCelebration_sequence()    

def Reset():
    print ("Reset")
    global StripVisual1, StripVisual2, StripAudio1, StripAudio2, jVisual1, jVisual2, jAudio1, jAudio2
    global AudioTime1, AudioTime2, VisualTime1, VisualTime2
    global LastResetTime
    global GameResetFlagVisual, GameResetFlagAudio
    global GameInProgress
    
    AudioGameInProgress = False
    VisualGameInProgress = False
    
    HoldingLights(StripVisual1, jVisual1)
    HoldingLights(StripVisual2, jVisual2)
    HoldingLights(StripAudio1, jAudio1)
    HoldingLights(StripAudio2, jAudio2)
    
    if GameResetFlagVisual == True:
        if VisualTime1 is None:
            sendText(1, 0, C_GREEN, MODE_SCROLL, scrolling_messageTryAgain, scrollspeed=ScrollPause, size = 1.5)
        else:
            sendText(1, 0, C_GREEN, MODE_RTEXT, str(int(VisualTime1)), scrollspeed=ScrollPause, size = 1.5)
    
        if VisualTime2 is None:
            sendText(2, 0, C_GREEN, MODE_SCROLL, scrolling_messageTryAgain, scrollspeed=ScrollPause, size = 1.5)
        else:
            sendText(2, 0, C_GREEN, MODE_RTEXT, str(int(VisualTime2)), scrollspeed=ScrollPause, size = 1.5)
    else:
        sendText(1, 0, C_GREEN, MODE_SCROLL, str(scrolling_messageNewVisual), scrollspeed=ScrollPause, size = 1.5)
        sendText(2, 0, C_GREEN, MODE_SCROLL, str(scrolling_messageNewVisual), scrollspeed=ScrollPause, size = 1.5)    
    
    if GameResetFlagAudio == True:
        if AudioTime1 is None: 
            sendText(1, 1, C_BLUE, MODE_SCROLL, scrolling_messageTryAgain, scrollspeed=ScrollPause, size = 1.5)
        else:
            sendText(1, 1, C_BLUE, MODE_RTEXT, str(int(AudioTime1)), scrollspeed=ScrollPause, size = 1.5)
    
        if AudioTime2 is None: 
            sendText(2, 1, C_BLUE, MODE_SCROLL, scrolling_messageTryAgain, scrollspeed=ScrollPause, size = 1.5)
        else:
            sendText(2, 1, C_BLUE, MODE_RTEXT, str(int(AudioTime2)), scrollspeed=ScrollPause, size = 1.5)
                
    else:
        print ("This should be the NewAudio message" +str(scrolling_messageNewAudio))
        sendText(1, 1, C_BLUE, MODE_SCROLL, str(scrolling_messageNewAudio), scrollspeed=ScrollPause, size = 1.5)
        sendText(2, 1, C_BLUE, MODE_SCROLL, str(scrolling_messageNewAudio), scrollspeed=ScrollPause, size = 1.5)

    GameResetFlagVisual = False
    GameResetFlagAudio = False
    RestartFlagVisual = False
    RestartFlagAudio = False

    
    React1Light.value(0)
    React2Light.value(0)
    
    LastResetTime = time.ticks_ms()
    

def FullReset():
    print ("FullReset")
    global StripVisual1, StripVisual2, StripAudio1, StripAudio2
    global LastResetTime
    global GameResetFlagVisual, GameResetFlagAudio
    
    Language = DefaultLanguage
    SetLanguage()
    
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
    
    sendText(1, 0, C_WHITE, MODE_SCROLL, scrolling_messageNewGame, scrollspeed=ScrollPause, size = 1.5)
    sendText(2, 0, C_WHITE, MODE_SCROLL, scrolling_messageNewGame, scrollspeed=ScrollPause, size = 1.5)
    sendClear(1,1)
    sendClear(2,1)
 
    LastResetTime = time.ticks_ms()



# Core code starts here

FullReset()

while True:
    GameInProgress = True
    print ("Starting a new game")

    while GameInProgress == True:
        
        if not LanguageButton.value():
            print ("Watching for language button")
            time.sleep(0.4)
            if Language == "English":
                Language = "Norwegian"
                SetLanguage()
                Reset()
                print ("Changing language to "+str(Language))
                print (scrolling_messageSoon)
            elif Language == "Norwegian":
                Language = "English"
                SetLanguage()
                Reset()
                print ("Changing language to "+str(Language))
                print (scrolling_messageSoon)
                
        if VisualRestartFlag == True:
            VisualGameInProgress = True
            AudioGameInProgress = False
            StartVisualGame()
        
        if not VisualGoButton.value():
            time.sleep(0.4) #s
            VisualGameInProgress = True
            AudioGameInProgress = False
            StartVisualGame()
            
        if AudioRestartFlag == True:
            AudioGameInProgress = True
            VisualGameInProgress = False
            StartAudioGame()
            
        if not AudioGoButton.value():
            time.sleep(0.4)
            AudioGameInProgress = True
            VisualGameInProgress = False
            StartAudioGame()
        
        if time.ticks_ms() - LastResetTime > FullResetInterval:
            FullReset()
            
            
    
    
#    GameInProgress = True



    
