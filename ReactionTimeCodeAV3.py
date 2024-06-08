# Libraries

import random
import neopixel
from machine import Pin, SPI, UART
import utime as time
#import max7219 
from picozero import Speaker
import _thread



# Set up the key variables we might want to tune

reaction_time = 1000  # ms #Typical reaction time for an 85 year old is 1s
wait_time = 2000  # ms Length of the ''ready' wait
random_wait_short = 2000 # Shortest time for the 'steady' wait
random_wait_long = 4000 # Longest time for the 'steady' wait

celebration_time = 5000  # ms
flash_time = 0.3 #s

FullResetInterval = 60000 # 3 minutes

ScrollPause = 0.05

Language = "Norwegian"

#Define the scrolling message
scrolling_messageSoon = "Too soon"
scrolling_messageSlow = "Too slow"
scrolling_messageVisualWait = "Press the button when the green light shows"
scrolling_messageAudioWait = "Press the button on the third beep"
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

resetDisplay0 = Pin(14, Pin.OUT)
resetDisplay0.value(1)
resetDisplay1 = Pin(10, Pin.OUT)
resetDisplay1.value(1)

#Speaker

speaker = Speaker(15)

# Set up the hardware

# Set up the LED strips

StripVisual1 = neopixel.NeoPixel(Pin(0), LED_num) #Visual1
StripVisual2 = neopixel.NeoPixel(Pin(4), LED_num) #Visual2
StripAudio1 = neopixel.NeoPixel(Pin(2), LED_num) #Audio1
StripAudio2 = neopixel.NeoPixel(Pin(3), LED_num) #Audio2

#Set up the displays
uarts = [
    UART(0, baudrate=9600, tx=Pin(012), rx=Pin(13)),
    UART(1, baudrate=9600, tx=Pin(08), rx=Pin(9))
    ]

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
    

# Display definitions

def resetDisplays():
    resetDisplay0.value(0)
    resetDisplay1.value(0)
    time.sleep(0.1)
    resetDisplay0.value(1)
    resetDisplay1.value(1)
    time.sleep(0.1)
    

# uart - a uart object
def setDisplayColour(display, half, colour):
    global uarts
    if display not in [0,1]:
        print("display must be 0 or 1 not "+str(display))
        return
    if half not in ["T", "B"]:
        print("half must be T or B not "+str(half))
        return
    if colour not in ["R", "G", "B", "Y", "W", "L"]:
        print("colour must be R,G,B,Y,W or L not "+str(colour))
        return
#    print(str(half)+"-C-"+str(colour))
    uarts[display].write(str(half)+"-C-"+str(colour)+"\n")
    
# mode
#    L - left justify
#    R - right justify
#    T - scrolling once
#    S - repeat scrolling
def setDisplayText(display, half, mode, text):
    global uarts
    if display not in [0,1]:
        print("display must be 0 or 1 not "+str(display))
        return
    if half not in ["T", "B"]:
        print("half must be T or B not "+str(half))
        return
    if mode not in ["L", "R", "T", "S"]:
        print("mode must be L, R, S or T")
#    print(str(half)+"-"+str(mode)+"-"+str(text))
    uarts[display].write(str(half)+"-"+str(mode)+"-"+str(text)+"\n")
    
def setTrafficLight(display, half, colour):
    global uarts
    if display not in [0,1]:
        print("display must be 0 or 1 not "+str(display))
        return
    if half not in ["T", "B"]:
        print("half must be T or B not "+str(half))
        return
    if colour not in ["R", "G", "Y",]:
        print("colour must be R,G or Y not "+str(colour))
        return
    
    uarts[display].write(str(half)+"-I-"+str(colour)+"\n")
    
    
# Display thread

def Displays():
    
    global TooSoon1, TooSoon2, TooSlow1, TooSlow2
    global VisualTime1, VisualTime2, AudioTime1, AudioTime2
    global VisualGameInProgress, AudioGameInProgress
    global scrolling_messageSoon
    global scrolling_messageSlow
    global scrolling_messageAudioWait
    global scrolling_messageVisualWait
    global scrolling_messageNewGame
    global scrolling_messageNewVisual
    global scrolling_messageNewAudio
    global PreGame_time, ReactWaiting, Celebrating
    global RedLight, AmberLight, GreenLight    
    global GameResetFlagAudio, GameResetFlagVisual    

    while VisualGameInProgress == True:
        
        if PreGame_time == True:
            setDisplayColour(0, "T", "G")
            setDisplayText(0, "T", "S", scrolling_messageVisualWait)
            setDisplayColour(1, "T", "G")
            setDisplayText(1, "T", "S", scrolling_messageVisualWait)

            setTrafficLight(0, "B", "R")
            setTrafficLight(1, "B", "R")
            
            while RedLight == True:
                if not React1Button.value(): 
                    setDisplayColour(0, "T", "R")
                    setDisplayText(0, "T", "S", scrolling_messageSoon)
                
                if not React2Button.value():
                    setDisplayColour(1, "T", "R")
                    setDisplayText(1, "T", "S", scrolling_messageSoon)
                    
                time.sleep(0.01)
                    
            setTrafficLight(0, "B", "Y")
            setTrafficLight(1, "B", "Y")
                
            while AmberLight == True:
                if not React1Button.value(): 
                    setDisplayColour(0, "T", "R")
                    setDisplayText(0, "T", "S", scrolling_messageSoon)
                
                if not React2Button.value():
                    setDisplayColour(1, "T", "R")
                    setDisplayText(1, "T", "S", scrolling_messageSoon)

                time.sleep(0.01)
                
                
        if ReactWaiting == True:
            
            setTrafficLight(0, "B", "G")
            setTrafficLight(1, "B", "G")
            
            while ReactWaiting == True:
            
                if not React1Button.value():
                    if VisualTime1 == None:
                        setDisplayColour(0, "B", "G")
                        setDisplayText(0, "B", "R", VisualTime1)
                
                if not React2Button.value():
                    if VisualTime1 == None:
                        setDisplayColour(1, "B", "G")
                        setDisplayText(1, "B", "R", VisualTime2)
                    
        if Celebrating == True:
            if TooSlow1 == True:
                setDisplayColour(0, "T", "R")
                setDisplayText(0, "T", "S", scrolling_messageSlow)
            if TooSoon1 == True:
                setDisplayColour(0, "T", "R")
                setDisplayText(0, "T", "S", scrolling_messageSoon)
            if TooSoon1 == False and TooSlow1 == False:
                setDisplayColour(0, "T", "G")
                setDisplayText(0, "T", "R", VisualTime1)
                
            if TooSlow2 == True:
                setDisplayColour(1, "T", "R")
                setDisplayText(1, "T", "S", scrolling_messageSlow)
            if TooSoon2 == True:
                setDisplayColour(1, "T", "R")
                setDisplayText(1, "T", "S", scrolling_messageSoon)
            if TooSoon2 == False and TooSlow2 == False:
                setDisplayColour(1, "T", "G")
                setDisplayText(1, "T", "R", VisualTime2)
                    
            if AudioTime1 is not None: 
                setDisplayColour(0, "B", "B")
                setDisplayText(0, "B", "R", AudioTime1)              
            else:
                setDisplayColour(0,"B", "B")
                setDisplayText(0, "B", "R", " ")
                
            if AudioTime2 is not None: 
                setDisplayColour(1, "B", "B")
                setDisplayText(1, "B", "R", AudioTime2)            
            else:
                setDisplayColour(1,"B", "B")
                setDisplayText(1, "B", "R", " ")
                                
            while Celebrating == True:
                time.sleep(0.1)
                    
                    
        
    while AudioGameInProgress == True:
                              
        if PreGame_time == True:
            setDisplayColour(0, "T", "B")
            setDisplayText(0, "T", "S", scrolling_messageAudioWait)
            setDisplayColour(1, "T", "B")
            setDisplayText(1, "T", "S", scrolling_messageAudioWait)
            
            setDisplayText(0, "B", "R", " ")
            setDisplayText(1, "B", "R", " ")
            
            while PreGame_time == True:
            
                if not React1Button.value(): # if the value changes
                    setDisplayColour(0, "T", "R")
                    setDisplayText(0, "T", "S", scrolling_messageSoon)
                    
                if not React2Button.value(): # if the value changes
                    setDisplayColour(1, "T", "R")
                    setDisplayText(1, "T", "S", scrolling_messageSoon)
                
                
        if ReactWaiting == True:
            
            while ReactWaiting == True:
            
                if not React1Button.value():
                    if AudioTime1 == None:
                        setDisplayColour(0, "B", "B")
                        setDisplayText(0, "B", "R", AudioTime1)
                
                if not React2Button.value():
                    if AudioTime2 == None:
                        setDisplayColour(1, "B", "B")
                        setDisplayText(1, "B", "R", AudioTime2)
                    
        if Celebrating == True:
            if TooSoon1 == True:
                setDisplayColour(0, "B", "B")
                setDisplayText(0, "B", "S", scrolling_messageSoon)            
            if TooSlow1 == True:
                setDisplayColour(0, "B", "B")
                setDisplayText(0, "B", "S", scrolling_messageSlow)
            if TooSlow1 == False and TooSoon1 == False:
                setDisplayColour(0, "B", "B")
                setDisplayText(0, "B", "R", AudioTime1)
                
            if TooSoon2 ==True:
                setDisplayColour(1, "B", "B")
                setDisplayText(1, "B", "S", scrolling_messageSoon) 
            if TooSlow2 == True:
                setDisplayColour(1, "B", "B")
                setDisplayText(1, "B", "S", scrolling_messageSlow)
            if TooSlow2 == False and TooSoon2 == False:
                setDisplayColour(1, "B", "B")
                setDisplayText(1, "B", "R", AudioTime2)
            
            if VisualTime1 is not None: 
                setDisplayColour(0, "T", "G")
                setDisplayText(0, "T", "R", VisualTime1)
            else:
                setDisplayColour(0, "T", "G")
                setDisplayText(0, "T", "R", " ")
                
            if VisualTime2 is not None: 
                setDisplayColour(1, "T", "G")
                setDisplayText(1, "T", "R", VisualTime2)
            else:
                setDisplayColour(1, "T", "G")
                setDisplayText(1, "T", "R", " ")

            while Celebrating == True:
                time.sleep(0.1)
                    
    if VisualGameInProgress == False and AudioGameInProgress == False:
        
        if GameResetFlagVisual == True:
            setDisplayColour(0, "T", "G")
            if VisualTime1 is None: 
                setDisplayText(0, "T", "S", scrolling_messageTryAgain)
            else:
                setDisplayText(0, "T", "R", VisualTime1)
    
            setDisplayColour(1, "T", "G")
            if VisualTime2 is None: 
                setDisplayText(1, "T", "S", scrolling_messageTryAgain)
            else:
                setDisplayText(1, "T", "R", VisualTime2)
        else:
            setDisplayColour(0, "T", "G")
            setDisplayText(0, "T", "S", "scrolling_messageNewVisual")
            
            setDisplayColour(1, "T", "G")
            setDisplayText(1, "T", "S", "scrolling_messageNewVisual")
            
        if GameResetFlagAudio == True:
            setDisplayColour(0, "B", "B")
            if AudioTime1 is None: 
                setDisplayText(0, "B", "S", scrolling_messageTryAgain)
            else:
                setDisplayText(0, "B", "R", AudioTime1)
    
            setDisplayColour(1, "B", "B")
            if AudioTime2 is None: 
                setDisplayText(1, "B", "S", scrolling_messageTryAgain)
            else:
                setDisplayText(1, "B", "R", AudioTime2)
                
        else:
            setDisplayColour(0, "B", "B")
            setDisplayText(0, "B", "S", "scrolling_messageNewAudio")
    
            setDisplayColour(1, "B", "B")
            setDisplayText(1, "B", "S", "scrolling_messageNewAudio")

  
 
        while VisualGameInProgress == False and AudioGameInProgress == False:
            time.sleep(0.1)


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
    global RedLight, AmberLight, GreenLight
    
    PreGame_time = True
    
    TooSoon1 = False
    TooSoon2 = False
    TooSlow1 = False
    TooSlow2 = False
    
    StripsOff(StripVisual1)
    StripsOff(StripVisual2)
    
    VisualGoButton.value(0)
    AudioGoButton.value(0)
    RedLight = True
    React1Light.value(1)
    React2Light.value(1)
    
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
            if not React2Button.value(): # if the value changes
                TooSoonLights(StripVisual2)
                TooSoon2 = True
                React2Light.value(0)
        
        RedLight = False
        AmberLight = True

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
            
            if not React2Button.value(): # if the value changes
                TooSoonLights(StripVisual2)
                TooSoon2 = True
                React2Light.value(0)
        
        if time.ticks_ms() - waiting_start > wait_time + random_wait:
            

            AmberLight = False
            GreenLight = True
            
            PreGame_time = False


def VisualGame_sequence():

    global ReactWaiting
    ReactWaiting = True
    
    global TooSoon1, TooSoon2, TooSlow1, TooSlow2
    global VisualTime1, VisualTime2
    global jVisual1, jVisual2
    global React1Waiting, React2Waiting
    global GameResetFlagVisual
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
                    
                if not React2Button.value():
                    if VisualTime2 == None:
                        VisualTime2 = time.ticks_ms()-start_time
                        React2Waiting = False
                        React2Light.value(0)

        ReactWaiting = False


    if React1Waiting == True:
        TooSlow1 = True
        VisualTime1 = None
    
    if React2Waiting == True:
        TooSlow2 = True
        VisualTime2 = None
    

    GreenLight = False


def VisualTime_output():
    global VisualTime1
    global VisualTime2

    if VisualTime1 is not None:
        displayVisual1.fill(0)
        displayVisual1.text('{0:04d}'.format(VisualTime1),0,0,1)
        displayVisual1.show()

    if VisualTime2 is not None:
        displayVisual2.fill(0)
        displayVisual2.text('{0:04d}'.format(VisualTime2),0,0,1)
        displayVisual2.show()

def VisualCelebration_sequence():

    global VisualGameInProgress
    global Celebrating
    
    Celebrating = True
               
    while Celebrating == True and VisualGameInProgress == True:
        global i
        FlashCounter = 0
        if not AudioGoButton.value():
            time.sleep(0.4) #s
            AudioGameInProgress = False
        if not VisualGoButton.value():
            time.sleep(0.4) #s
            VisualGameInProgress = False
            
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
            while FlashCounter < celebration_time/3/1000:
                time.sleep(3*flash_time)
                FlashCounter = FlashCounter + 1
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
    
    global TooSoon1
    global TooSoon2
    global TooSlow1
    global TooSlow2
    global AudioTime1
    global AudioTime2
    global AudioGameInProgress
    global RedLight, AmberLight, GreenLight

    
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
            if not React2Button.value(): # if the value changes
                React2Light.value(0)
                TooSoonLights(StripAudio2)
                TooSoon2 = True
                


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
#                Scroll()
                TooSoon1 = True           
            if not React2Button.value(): # if the value changes
                React1Light.value(0)
                TooSoonLights(StripAudio2)
#                Scroll()
                TooSoon2 = True
        
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
                if not React2Button.value():
                    if AudioTime2 == None:
                        AudioTime2 = time.ticks_ms()-start_time
                        React2Waiting = False
                        React2Light.value(0)
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



def AudioTime_output():
    global AudioTime1
    global AudioTime2
    
    if AudioTime1 is not None:
        displayAudio1.fill(0)
        displayAudio1.text('{0:04d}'.format(AudioTime1),0,0,1)
        displayAudio1.show()

    if AudioTime2 is not None:
        displayAudio2.fill(0)
        displayAudio2.text('{0:04d}'.format(AudioTime2),0,0,1)
        displayAudio2.show()
#        print ('AudioTime2')
#        print ('{0:04d}'.format(AudioTime2))
        

 

def AudioCelebration_sequence():

    global AudioGameInProgress
    global Celebrating
    
    Celebrating = True
               
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
            while FlashCounter < celebration_time/3/1000:
                time.sleep(3*flash_time)
                FlashCounter = FlashCounter + 1
            StripsOff(StripAudio1)
            StripsOff(StripAudio2)

        
        Celebrating = False
        AudioGameInProgress = False
        Reset()
            
    

def StartVisualGame():
    resetDisplays()
    print ('Visual Pre Game Sequence')
    VisualPreGame_sequence()
    print ('Visual Game Sequence')
    VisualGame_sequence()
    print ('Visual Celebration Sequence')
    VisualCelebration_sequence()
    
def StartAudioGame():
    resetDisplays()
    print ('Audio Pre Game Sequence')
    AudioPreGame_sequence()
    print ('Audio Game Sequence')
    AudioGame_sequence()
    print ('Audio Celebration Sequence')
    AudioCelebration_sequence()    

def Reset():
    
    print ('Reset')
    global StripVisual1, StripVisual2, StripAudio1, StripAudio2, jVisual1, jVisual2, jAudio1, jVisual2
    global AudioTime1, AudioTime2, VisualTime1, VisualTime2
    global LastResetTime
    
    HoldingLights(StripVisual1, jVisual1)
    HoldingLights(StripVisual2, jVisual2)
    HoldingLights(StripAudio1, jAudio1)
    HoldingLights(StripAudio2, jAudio2)
    

 


    React1Light.value(0)
    React2Light.value(0)
    RedLight = False
    AmberLight = False
    GreenLight = False
    
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
    RedLight = False
    AmberLight = False
    GreenLight = False
    
    VisualTime1 = None
    VisualTime2 = None
    AudioTime1 = None
    AudioTime2 = None

    jVisual1 = 0
    jVisual2 = 0
    jAudio1 = 0
    jAudio2 = 0
    resetDisplays()
    setDisplayColour(0, "T", "W")
    setDisplayText(0, "T", "S", scrolling_messageNewGame)
    setDisplayColour(1, "T", "W")
    setDisplayText(1, "T", "S", scrolling_messageNewGame)
    setDisplayColour(0, "B", "W")
    setDisplayText(0, "B", "R", " ")
    setDisplayColour(1, "B", "W")
    setDisplayText(1, "B", "R", " ")
    
    LastResetTime = time.ticks_ms()




# Set up the bits happening on the alternate thread
def CoreTask():
    while True:
        Displays()
        
_thread.start_new_thread(CoreTask, ())

FullReset()


while True:
    GameInProgress = True

    
    

    while GameInProgress == True and LastResetTime - time.ticks_ms() < FullResetInterval:
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
            
    FullReset()
    
#    GameInProgress = True



    