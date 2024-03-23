# Libraries

import random
import neopixel
from machine import Pin, SPI
import utime as time
import max7219 
from picozero import Speaker
import _thread


# Set pins
VisualGoButton = Pin(9, mode=Pin.IN, pull=Pin.PULL_UP)
AudioGoButton = Pin(8,mode=Pin.IN, pull=Pin.PULL_UP)
React1Button = Pin(7, mode=Pin.IN, pull=Pin.PULL_UP) 
React2Button = Pin(8, mode=Pin.IN, pull=Pin.PULL_UP)

#VisualGoLight = Pin(22, Pin.OUT)
#AudioGoLight = Pin(25, Pin.OUT)
#React1Light = Pin(4, Pin.OUT)
#React2Light = Pin(5, Pin.OUT)
RedLight = Pin(12, Pin.OUT)
AmberLight = Pin(13, Pin.OUT)
GreenLight = Pin(14, Pin.OUT)

speaker = Speaker(16)

#i2c_1 = I2C(id=1,scl=Pin(15),sda=Pin(16),freq=100000)   #set arbitrary pins for imaginary output
#lcd_1 = I2cLcd(i2c_1, 0x27, 2, 16)

#i2c_2 = I2C(id=2,scl=Pin(17),sda=Pin(18),freq=100000)   #set arbitrary pins for imaginary output
#lcd_2 = I2cLcd(i2c_2, 0x27, 2, 16)



    #Assume for now same number of LEDs on strips 1 and 2. 

StripVisual1 = neopixel.NeoPixel(Pin(1), LED_num) #Visual1
StripVisual2 = neopixel.NeoPixel(Pin(2), LED_num) #Visual2
StripAudio1 = neopixel.NeoPixel(Pin(4), LED_num) #Audio1
StripAudio2 = neopixel.NeoPixel(Pin(3), LED_num) #Audio2


#Set up the text display (just one for now..)

spi1 = SPI(0,sck=Pin(18),mosi=Pin(19))
cs1 = Pin(20, Pin.OUT)

display1 = max7219.Matrix8x8(spi1, cs1, 4)
display1.brightness(10)

# Set up the LED strips

LED_num = 70
BRIGHTNESS = 1.0

reaction_time = 1000  # ms #Typical reaction time for an 85 year old is 1s
wait_time = 2000  # ms
celebration_time = 5000  # ms

LED_interval = int (reaction_time/LED_num) #ms

jVisual1 = LED_num
jVisual2 = LED_num
jAudio1 = LED_num
jAudio2 = LED_num

# Definitions

# Light definitions

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
    if Strip == Visual1,Visual2:
        color = (0, 255, 0) 
        color = set_brightness(color)
        Strip.fill(color)
        Strip.write()
    # Blue fill
    elif Strip == Audio1, Audio 2:
        color = (0, 0, 255) 
        color = set_brightness(color)
        Strip.fill(color)
        Strip.write()
    
def TooSoonMatrix(Display):
    print ('For tidlig')
    Display.fill(0)
    Display.text('For tidlig',0,0,1)
    n=0
    while n < 65:
        Display.show()
        time.sleep(0.2)
        Display.scroll(-1,0)
        n = n + 1
        
def TooSlowMatrix(Display):
    print ('For sakte')
    Display.fill(0)
    Display.text('For sakte',0,0,1)
    n=0
    while n < 65:
        Display.show()
        time.sleep(0.2)
        Display.scroll(-1,0)
        n = n + 1        
        
def RisingLights():
    global jVisual1
    global jVisual2
    
    if TooSoon1 == True:
        jVisual1 = LED_num
    if TooSoon2 == True:
        jVisual2 = LED_num
    
    for j in range (0,i):
        
        if React1Waiting == True and TooSoon1 == False:
            StripVisual1[j]=(0,255,0)
            jVisual1 = j
            
        if React2Waiting == True and TooSoon2 == False:
            StripVisual2[j]=(0,255,0)
            jVisual2 = j
            
    StripVisual1.write()
    StripVisual2.write()
 

        
def Flash(Strip):
    
    if Strip == StripVisual1:
        k=jVisual1
    elif Strip == StripVisual2:
        k=jVisual2
    elif Strip == StripAudio1:
        k=jAudio1
    elif Strip == StripAudio2:
        k=jAudio2    
        
            #Display red Strip 1
    for l in range(k,LED_num):
        color = (255, 0, 0)  
        color = set_brightness(color)
        Strip[l]=(color)
    Strip.write()
    time.sleep(0.5) #s
        
            # Display green Strip 1
    for l in range(k,LED_num):    
        color = (0, 255, 0) 
        color = set_brightness(color)
        Strip[l]=(color)
    Strip.write()
    time.sleep(0.5) #s

            # Display blue Strip 1
    for l in range(k,LED_num):
        color = (0, 0, 255) 
        color = set_brightness(color)
        Strip[l]=(color)
    Strip.write()
    time.sleep(0.5) #s
        
def HoldingLights(Strip):
    global jVisual1, jVisual2, jAudio1, jAudio2
    global LED_num
    
    if Strip == StripVisual1:
        k=jVisual1
    elif Strip == StripVisual2:
        k=jVisual2
    elif Strip == StripAudio1:
        k=jAudio1
    elif Strip == StripAudio2:
        k=jAudio2
            
    #Only LEDs that lit during rising lights sequence stay on
  
    for l in range(k,LED_num):
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
        StripVisual1VisualTime = time.ticks_ms() #ms
#        React1Light.value(0)
    if (Strip == StripVisual2):
        StripVisual2VisualTime = time.ticks_ms() #ms
#        React2Light.value(0)
        
   
    
        
def VisualPreGame_sequence():

    
    PreGame_time = True
    
    global TooSoon1
    global TooSoon2
    global VisualGameInProgress
    
    TooSoon1 = False
    TooSoon2 = False
    
    StripsOff(StripVisual1)
    StripsOff(StripVisual2)

    RedLight.value(1)
    
    waiting_start = time.ticks_ms() #ms
    random_wait = random.randint(1000, 3000)
    
    while PreGame_time == True and VisualGameInProgress == True:

        if not VisualGoButton.value():
            time.sleep(0.4) #s
            VisualGameInProgress = False


        while time.ticks_ms() - waiting_start < wait_time and VisualGameInProgress == True:
            

            if not VisualGoButton.value():
                time.sleep(0.4) #s
                VisualGameInProgress = False

            
            if not React1Button.value(): # if the value changes
                TooSoonStrip(StripVisual1)
                TooSoon1 = True

                    
            if not React2Button.value(): # if the value changes
                TooSoonStrip(StripVisual2)
                TooSoon2 = True

        

        RedLight.value(0)
        AmberLight.value(1)
    
    
    
        while time.ticks_ms() - waiting_start < wait_time + random_wait and VisualGameInProgress == True:
            
            if not VisualGoButton.value():
                time.sleep(0.4)
                VisualGameInProgress = False


            if not React1Button.value(): # if the value changes
                TooSoonStrip(StripVisual1)
                TooSoon1 = True
            
            if not React2Button.value(): # if the value changes
                TooSoonStrip(StripVisual2)
                TooSoon2 = True
        
        
        if time.ticks_ms() - waiting_start > wait_time + random_wait:
            

            AmberLight.value(0)
            GreenLight.value(1)
        
#            React1Light.value(1)
#            React2Light.value(1)
            
            PreGame_time = False

def VisualGame_sequence():

    ReactWaiting = True
    
    global React1Waiting
    global React2Waiting
    
    global StripVisual1VisualTime
    global StripVisual2VisualTime
    
    global VisualGameInProgress
    
    global start_time
    global finish_time
    
    React1Waiting = True
    React2Waiting = True
    
    start_time = time.ticks_ms() #Records the current time
    
    while(ReactWaiting) and VisualGameInProgress == True:
        if not VisualGoButton.value():
            time.sleep(0.4) #s
            VisualGameInProgress = False

        global i
        i=1
        for i in range(1, LED_num):
            timeout = start_time + i * LED_interval


            RisingLights()

            while time.ticks_ms() < timeout:
                if not React1Button.value():
                    StripVisual1VisualTime = time.ticks_ms()
                    React1Waiting = False
                if not React2Button.value():
                    StripVisual2VisualTime = time.ticks_ms()
                    React2Waiting = False
                pass
            

        ReactWaiting = False

    if TooSoon1 == True:
        StripVisual1VisualTime = time.ticks_ms()
    
    if TooSoon2 == True:
        StripVisual2VisualTime = time.ticks_ms()

    if React1Waiting == True:
        StripVisual1VisualTime = time.ticks_ms()
    
    if React2Waiting == True:
        StripVisual2VisualTime = time.ticks_ms()
    

    finish_time = time.ticks_ms()
    GreenLight.value(0)



def VisualTime_output():
    global VisualTime1
    global VisualTime2
    VisualTime1 = StripVisual1VisualTime-start_time
    print ('VisualTime1')
    print (VisualTime1)
    print('{0:04d}'.format(VisualTime1))

    displayVisual1.fill(0)
    displayVisual1.text('{0:04d}'.format(VisualTime1),0,0,1)
    '{0:04d}'.format(VisualTime1)
    displayVisual1.show()

    VisualTime2 = StripVisual2VisualTime-start_time
    print ('VisualTime2')
    print (VisualTime2)
    print('{0:04d}'.format(VisualTime2))

    displayVisual2.fill(0)
    displayVisual2.text('{0:04d}'.format(VisualTime2),0,0,1)
    '{0:04d}'.format(VisualTime2)
    displayVisual2.show()
 
   

def VisualCelebration_sequence():

    global VisualGameInProgress
    Celebrating = True
    while Celebrating == True and VisualGameInProgress == True:
        global i
        FlashCounter = 0
        if not VisualGoButton.value():
            time.sleep(0.4) #s
            VisualGameInProgress = False
        if React1Waiting == False and TooSoon1 == False:

            if StripVisual1VisualTime < StripVisual2VisualTime:

                while FlashCounter < celebration_time/3/1000:
                    Flash(StripVisual1)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripVisual1)
                HoldingLights(StripVisual2)
                Celebrating = False
                VisualGameInProgress = False
            elif StripVisual1VisualTime == StripVisual2VisualTime:

                while FlashCounter < celebration_time/3/1000:
                    Flash(StripVisual1)
                    Flash(StripVisual2)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripVisual1)
                HoldingLights(StripVisual2)
                Celebrating = False
                VisualGameInProgress = False
            elif StripVisual1VisualTime>StripVisual2VisualTime:

                while FlashCounter < celebration_time/3/1000:
                    Flash(StripVisual2)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripVisual1)
                HoldingLights(StripVisual2)
                Celebrating = False
                VisualGameInProgress = False
            
        else:
            if React2Waiting == False and TooSoon2 ==False:

                while FlashCounter < celebration_time/3/1000:
                    Flash(StripVisual2)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripVisual1)
                HoldingLights(StripVisual2)
                Celebrating = False
                VisualGameInProgress = False
 
        
def AudioPreGame_sequence():
    waiting_start = time.ticks_ms() #ms
    random_wait = random.randint(1000, 3000)
    
    PreGame_time = True
    
    global TooSoon1
    global TooSoon2
    global AudioGameInProgress

    
    TooSoon1 = False
    TooSoon2 = False
    
    StripsOff(StripAudio1)
    StripsOff(StripAudio2)

    speaker.play('c4', 0.1) # play the middle c for 0.1 seconds
    print ('Beep1')
    

    
    while PreGame_time == True and AudioGameInProgress == True:

        if not AudioGoButton.value():
            time.sleep(0.4) #s
            AudioGameInProgress = False
        if not VisualGoButton.value():
            time.sleep(0.4) #s
            VisualGameInProgress = False


        while time.ticks_ms() - waiting_start < wait_time and AudioGameInProgress == True:
            

            if not AudioGoButton.value():
                time.sleep(0.4) #s
                AudioGameInProgress = False
            if not VisualGoButton.value():
                time.sleep(0.4) #s
                VisualGameInProgress = False

            
            if not React1Button.value(): # if the value changes
                TooSoonStrip(StripAudio1)
                Scroll()
                TooSoon1 = True

                    
            if not React2Button.value(): # if the value changes
                TooSoonStrip(StripAudio2)
                Scroll()
                TooSoon2 = True
                
            pass

        


        print ('Beep2')
        speaker.play('c4', 0.1) # play the middle c for 0.1 seconds

    
        while time.ticks_ms() - waiting_start < wait_time + random_wait and AudioGameInProgress == True:
            
            if not AudioGoButton.value():
                time.sleep(0.4) #s
                AudioGameInProgress = False
            if not VisualGoButton.value():
                time.sleep(0.4) #s
                VisualGameInProgress = False


            if not React1Button.value(): # if the value changes
                TooSoonStrip(StripAudio1)
                Scroll()
                TooSoon1 = True
            
            if not React2Button.value(): # if the value changes
                TooSoonStrip(StripAudio2)
                Scroll()
                TooSoon2 = True
        
        

            


        print ('Beeeeep')
        speaker.play('c4',0.2) # play the middle c for 0.1 seconds       
            
        PreGame_time = False

def AudioGame_sequence():

    ReactWaiting = True
    
    global React1Waiting
    global React2Waiting
    
    global StripAudio1Time
    global StripAudio2Time
    
    global AudioGameInProgress
    
    global start_time
    global finish_time
    
    React1Waiting = True
    React2Waiting = True

    
    start_time = time.ticks_ms() #Records the current time
    
    while(ReactWaiting) and AudioGameInProgress == True:
        if not AudioGoButton.value():
            time.sleep(0.4) #s
            AudioGameInProgress = False
        if not VisualGoButton.value():
            time.sleep(0.4) #s
            VisualGameInProgress = False

        global i
        global jAudio1
        global jAudio2
        
        i=1
        for i in range(1, LED_num):
            timeout = start_time + i * LED_interval
        
    
            if TooSoon1 == True:
                jAudio1 = LED_num
            if TooSoon2 == True:
                jAudio2 = LED_num
        
            if React1Waiting == True and TooSoon1 == False:
                jAudio1 = i
            
            if React2Waiting == True and TooSoon2 == False:           
                jAudio2 = i

            while time.ticks_ms() < timeout:
                if not React1Button.value():
                    StripAudio1Time = time.ticks_ms()
                    React1Waiting = False
                if not React2Button.value():
                    StripAudio2Time = time.ticks_ms()
                    React2Waiting = False
                pass
            

        ReactWaiting = False
    
    finish_time = time.ticks_ms()
    
    if TooSoon1 == False:
        for j in range (0,jAudio1):
            StripAudio1[j]=(0,0,255)
        StripAudio1.write()    
            
    if TooSoon2 == False:      
        for j in range (0,jAudio2):
            StripAudio2[j]=(0,0,255)
        StripAudio2.write()   

    if TooSoon1 == True:
        StripAudio1Time = time.ticks_ms()
    
    if TooSoon2 == True:
        StripAudio2Time = time.ticks_ms()

    if React1Waiting == True:
        StripAudio1Time = time.ticks_ms()
    
    if React2Waiting == True:
        StripAudio2Time = time.ticks_ms()
    

    



def AudioTime_output():
    global AudioTime1
    global AudioTime2
    AudioTime1 = StripAudio1Time-start_time
    print ('AudioTime1')
    print (AudioTime1)
    print('{0:04d}'.format(AudioTime1))
    
    displayAudio1.fill(0)
    displayAudio1.text('{0:04d}'.format(AudioTime1),0,0,1)
    '{0:04d}'.format(AudioTime1)
    displayAudio1.show()



    AudioTime2 = StripAudio2Time-start_time
    print ('AudioTime2')
    print (AudioTime2)
    print('{0:04d}'.format(AudioTime2))

    displayAudio2.fill(0)
    displayAudio2.text('{0:04d}'.format(AudioTime2),0,0,1)
    '{0:04d}'.format(AudioTime2)
    displayAudio2.show() 

 
#    while True:
#        lcd.move_to(0,0)
#        lcd.putstr('Hello world')
    
#        lcd.clear()                # Clear display    

def AudioCelebration_sequence():

    global AudioGameInProgress
    Celebrating = True
    
    
                
    while Celebrating == True and AudioGameInProgress == True:
        global i
        FlashCounter = 0
        if not AudioGoButton.value():
            time.sleep(0.4) #s
            AudioGameInProgress = False
        if not VisualGoButton.value():
            time.sleep(0.4) #s
            VisualGameInProgress = False
            
        if React1Waiting == False and TooSoon1 == False:

            if StripAudio1Time < StripAudio2Time:
                while FlashCounter < celebration_time/3/1000:
                    Flash(StripAudio1)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripAudio1)
                HoldingLights(StripAudio2)
                Celebrating = False
                AudioGameInProgress = False
                
            elif StripAudio1Time == StripAudio2Time:
                while FlashCounter < celebration_time/3/1000:
                    Flash(StripAudio1)
                    Flash(StripAudio2)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripAudio1)
                HoldingLights(StripAudio2)
                Celebrating = False
                AudioGameInProgress = False
                
            elif StripAudio1Time>StripAudio2Time:

                while FlashCounter < celebration_time/3/1000:
                    Flash(StripAudio2)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripAudio1)
                HoldingLights(StripAudio2)
                Celebrating = False
                AudioGameInProgress = False
            
        else:
            if React2Waiting == False and TooSoon2 ==False:

                while FlashCounter < celebration_time/3/1000:
                    Flash(StripAudio2)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripAudio1)
                HoldingLights(StripAudio2)
                Celebrating = False
                AudioGameInProgress = False    

    
    
def StartVisualGame():
    
    print ('Visual Pre Game Sequence')
    VisualPreGame_sequence()
    print ('Visual Game Sequence')
    VisualGame_sequence()
    print ('Time output')
    VisualTime_output()
    print ('Visual Celebration Sequence')
    VisualCelebration_sequence()
    
def StartAudioGame():
    
    print ('Audio Pre Game Sequence')
    AudioPreGame_sequence()
    print ('Audio Game Sequence')
    AudioGame_sequence()
    print ('Time output')
    AudioTime_output()
    print ('Audio Celebration Sequence')
    AudioCelebration_sequence()    

def Reset():
    global StripVisual1, StripVisual2, StripAudio1, StripAudio2

    HoldingLights(StripVisual1)
    HoldingLights(StripVisual2)
    HoldingLights(StripAudio1)
    HoldingLights(StripAudio2)

#    React1Light.value(0)
#    React2Light.value(0)
    RedLight.value(0)
    AmberLight.value(0)
    GreenLight.value(0)

    
    
# StartGame

GameInProgress = True

#Turn off all the lights
StripsOff(StripVisual1)
StripsOff(StripVisual2)
StripsOff(StripAudio1)
StripsOff(StripAudio2)

#React1Light.value(0)
#React2Light.value(0)
RedLight.value(0)
AmberLight.value(0)
GreenLight.value(0)

jVisual1 = 0
jVisual2 = 0
jAudio1 = 0
jAudio2 = 0

while GameInProgress == True:
    if not VisualGoButton.value():
        VisualGameInProgress = True
        AudioGameInProgress = False
        time.sleep(0.4) #s
        StartVisualGame()
        print ('StartVisualGame')
        Reset()
        
    if not AudioGoButton.value():
        print ('AudioGoButton')
        AudioGameInProgress = True
        VisualGameInProgress = False
        time.sleep(0.4)
        StartAudioGame()
        print ('StartAudioGame')
        Reset()
    
#    GameInProgress = True




    
        
        

	






