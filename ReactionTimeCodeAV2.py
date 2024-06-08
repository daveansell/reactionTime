# Libraries

import random
import neopixel
from machine import Pin, SPI
import utime as time
import max7219 
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

#Define the scrolling message
scrolling_messageSoon = "For tidlig"
scrolling_messageSlow = "For sakte"

if len(scrolling_messageSoon)>len(scrolling_messageSlow):
    message_length = len(scrolling_messageSoon)
else:
    message_length = len(scrolling_messageSlow)
    
message_column = message_length*8

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

VisualGoButton = Pin(9, mode=Pin.IN, pull=Pin.PULL_UP)
AudioGoButton = Pin(27,mode=Pin.IN, pull=Pin.PULL_UP)
React1Button = Pin(6, mode=Pin.IN, pull=Pin.PULL_UP) 
React2Button = Pin(8, mode=Pin.IN, pull=Pin.PULL_UP)

# Button lights

VisualGoLight = Pin(17, Pin.OUT)
AudioGoLight = Pin(11, Pin.OUT)
React1Light = Pin(10, Pin.OUT)
React2Light = Pin(10, Pin.OUT)

# Traffic lights

RedLight = Pin(12, Pin.OUT)
AmberLight = Pin(13, Pin.OUT)
GreenLight = Pin(14, Pin.OUT)

#Speaker

speaker = Speaker(16)

# Set up the hardware

# Set up the LED strips

StripVisual1 = neopixel.NeoPixel(Pin(2), LED_num) #Visual1
StripVisual2 = neopixel.NeoPixel(Pin(4), LED_num) #Visual2
StripAudio1 = neopixel.NeoPixel(Pin(3), LED_num) #Audio1
StripAudio2 = neopixel.NeoPixel(Pin(5), LED_num) #Audio2

#Set up the text displays

spiVisual1 = SPI(0,sck=Pin(18),mosi=Pin(19))
csVisual1 = Pin(21, Pin.OUT)
displayVisual1 = max7219.Matrix8x8(spiVisual1, csVisual1, 4)
displayVisual1.brightness(VisualMatrixBrightness)

spiVisual2 = SPI(0,sck=Pin(18),mosi=Pin(19))
csVisual2 = Pin(26, Pin.OUT)
displayVisual2 = max7219.Matrix8x8(spiVisual2, csVisual2, 4)
displayVisual2.brightness(VisualMatrixBrightness)

spiAudio1 = SPI(0,sck=Pin(18),mosi=Pin(19))
csAudio1 = Pin(20, Pin.OUT)
displayAudio1 = max7219.Matrix8x8(spiAudio1, csAudio1, 4)
displayAudio1.brightness(AudioMatrixBrightness)

spiAudio2 = SPI(0,sck=Pin(18),mosi=Pin(19))
csAudio2 = Pin(22, Pin.OUT)
displayAudio2 = max7219.Matrix8x8(spiAudio2, csAudio2, 4)
displayAudio2.brightness(AudioMatrixBrightness)

# Definitions

# Light definitions

# Set inital flags etc
GameInProgress = True
PreGame_time = False
VisualGameInProgress = False
AudioGameInProgress = False
ReactWaiting = False
Celebrating = False


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
    
    
# Matrix definitions

def Matrices():
    
    global TooSoon1
    global TooSoon2
    global TooSlow1
    global TooSlow2
    global VisualGameInProgress
    global AudioGameInProgress
    global ScrollPause
    global scrolling_messageSoon
    global scrolling_messageSlow
    global message_length
    global PreGame_time
    
    
    while VisualGameInProgress == True:
        if not VisualGoButton.value():
            time.sleep(0.4) #s
            max7219.init()
            VisualGameInProgress = False
        if not AudioGoButton.value():
            time.sleep(0.4) #s
            max7219.init()
            VisualGameInProgress = False

        display1 = displayVisual1
        display2 = displayVisual2
                
  
        display1.fill(0)
        display1.show()
        

        display2.fill(0)
        display2.show()
        
        time.sleep(ScrollPause)

        for x in range(32, -message_column, -1):     
        #Clear the display
        # Write the scrolling text in to frame buffer
        #Display the message
        
            if not React1Button.value():
                time.sleep(0.4) #s
                VisualTime_output()
            if not React2Button.value():
                time.sleep(0.4) #s
                VisualTime_output()
                
            if PreGame_time == True:
                display1.fill(0)
                display2.fill(0)
                display1.show()
                display2.show()
                print ('Blank')
        
            if TooSoon1 == True: 
                display1.fill(0)
                display1.text(scrolling_messageSoon,x,0,1)
                display1.show()
                print ('TooSoon1')
            if TooSoon2 == True: 
                display2.fill(0)
                display2.text(scrolling_messageSoon,x,0,1)
                display2.show()
                print ('TooSoon2')
            if TooSlow1 == True: 
                display1.fill(0)
                display1.text(scrolling_messageSlow,x,0,1)
                display1.show()
                print ('TooSlow2')
            if TooSlow2 == True: 
                display2.fill(0)
                display2.text(scrolling_messageSlow,x,0,1)
                display2.show()
                print ('TooSlow2')

            time.sleep(ScrollPause)
        
    while AudioGameInProgress == True:
        if not VisualGoButton.value():
            time.sleep(0.4) #s
            AudioGameInProgress = False
        if not AudioGoButton.value():
            time.sleep(0.4) #s
            AudioGameInProgress = False
        display1 = displayAudio1
        display2 = displayAudio2
                
        if TooSoon1 == True or TooSlow1 == True:   
            display1.fill(0)
            display1.show()
        
        if TooSoon2 == True or TooSlow2 == True:
            display2.fill(0)
            display2.show()
        #sleep for one one seconds
        time.sleep(ScrollPause)

        for x in range(32, -message_column, -1):     
        #Clear the display
            
            
            if not React1Button.value():
                time.sleep(0.4) #s
                AudioTime_output()
            if not React2Button.value():
                time.sleep(0.4) #s
                AudioTime_output()
                
            if PreGame_time == True:
                display1.fill(0)
                display2.fill(0)
                display1.show()
                display2.show()
                print ('Blank')
                
        # Write the scrolling text in to frame buffer
        #Display the message
            if TooSoon1 == True: 
                display1.fill(0)
                display1.text(scrolling_messageSoon,x,0,1)
                display1.show()
            if TooSoon2 == True: 
                display2.fill(0)
                display2.text(scrolling_messageSoon,x,0,1)
                display2.show()
            if TooSlow1 == True: 
                display1.fill(0)
                display1.text(scrolling_messageSlow,x,0,1)
                display1.show()
            if TooSlow2 == True: 
                display2.fill(0)
                display2.text(scrolling_messageSlow,x,0,1)
                display2.show()

            time.sleep(ScrollPause)        
                
                
#def TimeMatrix(Display,Timer):
#    Display.fill(0)
#    Display.text('{0:04d}'.format(Timer),0,0,1)
#    Display.show()
    

    
    
#def BlankDisplay(Display):
#    Display.fill(0)
#    Display.show()

#Timer (I don't think this is in use at the moment..)

def StopTimer(Strip):
    if (Strip == StripVisual1):
        Visual1Time = time.ticks_ms() #ms
#        React1Light.value(0)

    if (Strip == StripVisual2):
        Visual2Time = time.ticks_ms() #ms
#        React2Light.value(0)
    

    if (Strip == StripAudio1):
        Audio1Time = time.ticks_ms() #ms
#        React1Light.value(0)

    if (Strip == StripVAudio2):
        Audio2Time = time.ticks_ms() #ms
#        React2Light.value(0)




# Game sections

def VisualPreGame_sequence():

    PreGame_time = True
    
    global wait_time
    global TooSoon1, TooSoon2, TooSlow1, TooSlow2
    global VisualGameInProgress
    
    TooSoon1 = False
    TooSoon2 = False
    TooSlow1 = False
    TooSlow2 = False
    
    StripsOff(StripVisual1)
    StripsOff(StripVisual2)
    
    VisualGoButton.value(0)
    AudioGoButton.value(0)
    RedLight.value(1)
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
        
        RedLight.value(0)
        AmberLight.value(1)

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
            

            AmberLight.value(0)
            GreenLight.value(1)
            
            PreGame_time = False


def VisualGame_sequence():

    ReactWaiting = True
    
    global TooSoon1, TooSoon2, TooSlow1, TooSlow2
    global VisualTime1, VisualTime2
    global jVisual1, jVisual2
    global React1Waiting, React2Waiting
    jVisual1 = 0
    jVisual2 = 0
    
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
                    VisualTime1 = time.ticks_ms()-start_time
                    React1Waiting = False
                    React1Light.value(0)
                    
                if not React2Button.value():
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
    

    GreenLight.value(0)


def VisualTime_output():
    global VisualTime1
    global VisualTime2

    if VisualTime1 is not None:
        displayVisual1.fill(0)
        displayVisual1.text('{0:04d}'.format(VisualTime1),0,0,1)
        displayVisual1.show()
        print ('VisualTime1')
        print ('{0:04d}'.format(VisualTime1))

    if VisualTime2 is not None:
        displayVisual2.fill(0)
        displayVisual2.text('{0:04d}'.format(VisualTime2),0,0,1)
        displayVisual2.show()
        print ('VisualTime2')
        print ('{0:04d}'.format(VisualTime2))
    
def VisualCelebration_sequence():

    global VisualGameInProgress
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

def AudioPreGame_sequence():
    waiting_start = time.ticks_ms() #ms
    random_wait = random.randint(1000, 3000)
    
    PreGame_time = True
    
    global TooSoon1
    global TooSoon2
    global TooSlow1
    global TooSlow2
    global AudioTime1
    global AudioTime2
    global AudioGameInProgress

    
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
    ReactWaiting = True
    
    global TooSoon1, TooSoon2, TooSlow1, TooSlow2
    global AudioTime1, AudioTime2
    global jAudio1, jAudio2
    global React1Waiting, React2Waiting
    global i
    jAudio1 = 0
    jAudio2 = 0
    
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
                    AudioTime1 = time.ticks_ms()-start_time
                    React1Waiting = False
                    React1Light.value(0)
                if not React2Button.value():
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
        print ('AudioTime1')
        print ('{0:04d}'.format(AudioTime1))

    if AudioTime2 is not None:
        displayAudio2.fill(0)
        displayAudio2.text('{0:04d}'.format(AudioTime2),0,0,1)
        displayAudio2.show()
        print ('AudioTime2')
        print ('{0:04d}'.format(AudioTime2))
        

 

def AudioCelebration_sequence():

    global AudioGameInProgress
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
#                print ('AudioTime1 < AudioTime2')
                while FlashCounter < celebration_time/3/1000:
                    Flash(StripAudio1,jAudio1)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripAudio1,jAudio1)
                HoldingLights(StripAudio2,jAudio2)

                
                
            elif AudioTime1 == AudioTime2:
#                print ('AudioTime1 == AudioTime2')
                while FlashCounter < celebration_time/3/1000:
                    Flash(StripAudio1,jAudio1)
                    Flash(StripAudio2,jAudio2)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripAudio1,jAudio1)
                HoldingLights(StripAudio2,jAudio2)

                
                
            elif AudioTime1>AudioTime2:
#                print ('AudioTime1>AudioTime2')
                while FlashCounter < celebration_time/3/1000:
                    Flash(StripAudio2,jAudio2)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripAudio1,jAudio1)
                HoldingLights(StripAudio2,jAudio2)

                
            
        elif AudioTime1 is None and AudioTime2 is not None:
#                print ('AudioTime1 is None and AudioTime2 is not None')
                while FlashCounter < celebration_time/3/1000:
                    Flash(StripAudio2,jAudio2)
                    FlashCounter = FlashCounter + 1
                StripsOff(StripAudio1)
                HoldingLights(StripAudio2,jAudio2)

                
                
        elif AudioTime1 is not None and AudioTime2 is None:
#            print ('AudioTime1 is not None and AudioTime2 is Non')
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
            
    

def StartVisualGame():
    print ('Visual Pre Game Sequence')
    VisualPreGame_sequence()
    print ('Visual Game Sequence')
    VisualGame_sequence()
#    print ('Time output')
#    VisualTime_output()
    print ('Visual Celebration Sequence')
    VisualCelebration_sequence()
    
def StartAudioGame():
    print ('Audio Pre Game Sequence')
    AudioPreGame_sequence()
    print ('Audio Game Sequence')
    AudioGame_sequence()
#    print ('Time output')
#    AudioTime_output()
    print ('Audio Celebration Sequence')
    AudioCelebration_sequence()    

def Reset():
    
    print ('Reset')
    global StripVisual1, StripVisual2, StripAudio1, StripAudio2, jVisual1, jVisual2, jAudio1, jVisual2
    global LastResetTime
    
    HoldingLights(StripVisual1, jVisual1)
    HoldingLights(StripVisual2, jVisual2)
    HoldingLights(StripAudio1, jAudio1)
    HoldingLights(StripAudio2, jAudio2)

    React1Light.value(0)
    React2Light.value(0)
    RedLight.value(0)
    AmberLight.value(0)
    GreenLight.value(0)
    
    LastResetTime = time.ticks_ms()
    
    


def FullReset():
    print ('Full Reset')
    global StripVisual1, StripVisual2, StripAudio1, StripAudio2

    StripsOff(StripVisual1)
    StripsOff(StripVisual2)
    StripsOff(StripAudio1)
    StripsOff(StripAudio2)

    React1Light.value(0)
    React2Light.value(0)
    RedLight.value(0)
    AmberLight.value(0)
    GreenLight.value(0)
    
    VisualTime1 = None
    VisualTime2 = None
    AudioTime1 = None
    AudioTime2 = None

    jVisual1 = 0
    jVisual2 = 0
    jAudio1 = 0
    jAudio2 = 0



# Set up the bits happening on the alternate thread
def CoreTask():
    while True:
        Matrices()
        
_thread.start_new_thread(CoreTask, ())

FullReset()
LastResetTime = time.ticks_ms()

while True:
    GameInProgress = True

    
    

    while GameInProgress == True and LastResetTime - time.ticks_ms() < FullResetInterval:
        if not VisualGoButton.value():
            Reset()
            time.sleep(0.4) #s
            VisualGameInProgress = True
            AudioGameInProgress = False
            print ('StartVisualGame')
            StartVisualGame()
            
        if not AudioGoButton.value():
            Reset()
            time.sleep(0.4)
            AudioGameInProgress = True
            VisualGameInProgress = False
            print ('StartAudioGame')
            StartAudioGame()
            
    FullReset()
    
#    GameInProgress = True



    