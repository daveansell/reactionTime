# Libraries

import random
import neopixel
import machine
from machine import Pin, I2C
import utime as time
from pico_i2c_lcd import I2cLcd
from picozero import Speaker


# Set pins
VisualGoButton = Pin(9, mode=Pin.IN, pull=Pin.PULL_UP)
AudioGoButton = Pin(8,mode=Pin.IN, pull=Pin.PULL_UP)
React1Button = Pin(7, mode=Pin.IN, pull=Pin.PULL_UP) 
React2Button = Pin(8, mode=Pin.IN, pull=Pin.PULL_UP)

#GoLight = Pin(25, Pin.OUT)
#React1Light = Pin(4, Pin.OUT)
#React2Light = Pin(5, Pin.OUT)
RedLight = Pin(12, Pin.OUT)
AmberLight = Pin(13, Pin.OUT)
GreenLight = Pin(14, Pin.OUT)

speaker = machine.Pin(16, Pin.OUT)

#i2c_1 = I2C(id=1,scl=Pin(15),sda=Pin(16),freq=100000)   #set arbitrary pins for imaginary output
#lcd_1 = I2cLcd(i2c_1, 0x27, 2, 16)

#i2c_2 = I2C(id=2,scl=Pin(17),sda=Pin(18),freq=100000)   #set arbitrary pins for imaginary output
#lcd_2 = I2cLcd(i2c_2, 0x27, 2, 16)


# Set up the LED strips

LED_num = 70
    #Assume for now same number of LEDs on strips 1 and 2. 

StripVisual1 = neopixel.NeoPixel(Pin(2), LED_num) #Visual1
StripVisual2 = neopixel.NeoPixel(Pin(1), LED_num) #Visual2
StripAudio1 = neopixel.NeoPixel(Pin(4), LED_num) #Audio1
StripAudio2 = neopixel.NeoPixel(Pin(3), LED_num) #Audio2

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

#Sound definitions

@rp2.asm_pio(
    set_init=rp2.PIO.OUT_LOW,
    in_shiftdir=rp2.PIO.SHIFT_LEFT,
    out_shiftdir=rp2.PIO.SHIFT_LEFT,
)
def wave_prog():
    pull(block)
    mov(x, osr)         # waveCount
    pull(block)
    label("loop")
    mov(y, osr)         # halfWaveNumCycles
    set(pins, 1)        # high
    label("high")
    jmp(y_dec, "high")
    mov(y, osr)         # halfWaveNumCycles
    set(pins, 0)        # low
    label("low")
    jmp(y_dec, "low")
    jmp(x_dec, "loop")
# the clock frequency of Raspberry Pi Pico is 125MHz; 1953125 is 125MHz / 64
sm = rp2.StateMachine(0, wave_prog, freq=1953125, set_base=Pin(16)) 
sm.active(1)
def HWPlayTone(freq: int, duration: int):
    # count 1 cycle for jmp() ==> 1 cycle per half wave ==> 2 cycles per wave
    halfWaveNumCycles = round(1953125.0 / freq / 2)
    waveCount = round(duration * freq / 1000.0)
    sm.put(waveCount)
    sm.put(halfWaveNumCycles)


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
        StripVisual1Time = time.ticks_ms() #ms
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
                TooSoon(StripVisual1)
                TooSoon1 = True

                    
            if not React2Button.value(): # if the value changes
                TooSoon(StripVisual2)
                TooSoon2 = True

        

        RedLight.value(0)
        AmberLight.value(1)
    
    
    
        while time.ticks_ms() - waiting_start < wait_time + random_wait and VisualGameInProgress == True:
            
            if not VisualGoButton.value():
                time.sleep(0.4)
                VisualGameInProgress = False


            if not React1Button.value(): # if the value changes
                TooSoon(StripVisual1)
                TooSoon1 = True
            
            if not React2Button.value(): # if the value changes
                TooSoon(StripVisual2)
                TooSoon2 = True
        
        
        if time.ticks_ms() - waiting_start > wait_time + random_wait:
            
            PreGame_time = False

def VisualGame_sequence():
    
    AmberLight.value(0)
    GreenLight.value(1)

    ReactWaiting = True
    
    global React1Waiting
    global React2Waiting
    
    global StripVisual1Time
    global StripVisual2VisualTime
    
    global VisualGameInProgress
    
    global start_time
    global finish_time
    
    React1Waiting = True
    React2Waiting = True
    
    start_time = time.ticks_ms() #Records the current time
    
    print (LED_interval)
    print (LED_num)
    
    while(ReactWaiting) and VisualGameInProgress == True:

        global i
        i=1
        for i in range(1, LED_num):
            timeout = start_time + i * LED_interval

            RisingLights()

            while time.ticks_ms() < timeout:
                if not React1Button.value():
                    StripVisual1Time = time.ticks_ms()
                    React1Waiting = False
                if not React2Button.value():
                    StripVisual2VisualTime = time.ticks_ms()
                    React2Waiting = False  

        ReactWaiting = False
        print (i)
        
    finish_time = time.ticks_ms()
    
    if TooSoon1 == True:
        StripVisual1Time = start_time
    
    if TooSoon2 == True:
        StripVisual2VisualTime = start_time

    if React1Waiting == True:
        StripVisual1Time = finish_time
    
    if React2Waiting == True:
        StripVisual2VisualTime = finish_time
    

    
    GreenLight.value(0)



def VisualTime_output():

    VisualTime1 = StripVisual1Time-start_time
    print ('VisualTime1')
    print (VisualTime1)
    print('{0:04d}'.format(VisualTime1))

#    lcd_1.move_to(0,0)
#    lcd_1.putstr('Visual:')
#    lcd_1.move_to(8,0)
#    lcd_1.putstr('{0:04d}'.format(VisualTime1))


    VisualTime2 = StripVisual2VisualTime-start_time
    print ('VisualTime2')
    print (VisualTime2)
    print('{0:04d}'.format(VisualTime2))

#    lcd_2.move_to(0,0)
#    lcd_2.putstr('Visual:')
#    lcd_2.move_to(8,0)
#    lcd_2.putstr('{0:04d}'.format(VisualTime2))   

 
#    while True:
#        lcd.move_to(0,0)
#        lcd.putstr('Hello world')
    
#        lcd.clear()                # Clear display    

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

            if StripVisual1Time < StripVisual2VisualTime:

                while FlashCounter < celebration_time/3/1000:
                    Flash(StripVisual1)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripVisual1)
                HoldingLights(StripVisual2)
                Celebrating = False
                VisualGameInProgress = False
            elif StripVisual1Time == StripVisual2VisualTime:

                while FlashCounter < celebration_time/3/1000:
                    Flash(StripVisual1)
                    Flash(StripVisual2)
                    FlashCounter = FlashCounter + 1
                HoldingLights(StripVisual1)
                HoldingLights(StripVisual2)
                Celebrating = False
                VisualGameInProgress = False
            elif StripVisual1Time>StripVisual2VisualTime:

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

    HWPlayTone(262, 100) # play the middle c for 0.1 seconds
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
                TooSoon(StripAudio1)
                TooSoon1 = True
                print ('Audio1TooSoon')

                    
            if not React2Button.value(): # if the value changes
                TooSoon(StripAudio2)
                TooSoon2 = True
                print ('Audio2TooSoon')
                


        


        print ('Beep2')
        HWPlayTone(262, 100) # play the middle c for 0.1 seconds

    
        while time.ticks_ms() - waiting_start < wait_time + random_wait and AudioGameInProgress == True:
            
            if not AudioGoButton.value():
                time.sleep(0.4) #s
                AudioGameInProgress = False
            if not VisualGoButton.value():
                time.sleep(0.4) #s
                VisualGameInProgress = False


            if not React1Button.value(): # if the value changes
                TooSoon(StripAudio1)
                TooSoon1 = True
            
            if not React2Button.value(): # if the value changes
                TooSoon(StripAudio2)
                TooSoon2 = True
            
        PreGame_time = False

def AudioGame_sequence():
    
    print ('Beeeeep')
    HWPlayTone(262, 300) # play the middle c for 0.1 seconds

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

    print (LED_interval)
    print (LED_num)
    
    start_time = time.ticks_ms() #Records the current time
    
    while(ReactWaiting) and AudioGameInProgress == True:

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
                
            
        print (i)
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
        StripAudio1Time = 0
    
    if TooSoon2 == True:
        StripAudio2Time = 0

    if React1Waiting == True:
        StripAudio1Time = finish_time
    
    if React2Waiting == True:
        StripAudio2Time = finish_time
        
     
    

    



def AudioTime_output():

    AudioTime1 = StripAudio1Time-start_time
    print ('AudioTime1')
    print (AudioTime1)
    print('{0:04d}'.format(AudioTime1))

#    lcd_1.move_to(0,0)
#    lcd_1.putstr('Audio:')
#    lcd_1.move_to(8,0)
#    lcd_1.putstr('{0:04d}'.format(AudioTime1))


    AudioTime2 = StripAudio2Time-start_time
    print ('AudioTime2')
    print (AudioTime2)
    print('{0:04d}'.format(AudioTime2))

#    lcd_2.move_to(0,0)
#    lcd_2.putstr('Audio:')
#    lcd_2.move_to(8,0)
#    lcd_2.putstr('{0:04d}'.format(AudioTime2))   

 
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




    
        
        

	






