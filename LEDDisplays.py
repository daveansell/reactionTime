from machine import Pin, SPI
import max7219
import utime as time

VisualMatrixBrightness = 15
AudioMatrixBrightness = 15

spiVisual1 = SPI(0,sck=Pin(18),mosi=Pin(19))
csVisual1 = Pin(20, Pin.OUT)
displayVisual1 = max7219.Matrix8x8(spiVisual1, csVisual1, 4)
displayVisual1.brightness(VisualMatrixBrightness)

spiVisual2 = SPI(0,sck=Pin(18),mosi=Pin(19))
csVisual2 = Pin(22, Pin.OUT)
displayVisual2 = max7219.Matrix8x8(spiVisual2, csVisual2, 4)
displayVisual2.brightness(VisualMatrixBrightness)

spiAudio1 = SPI(0,sck=Pin(18),mosi=Pin(19))
csAudio1 = Pin(21, Pin.OUT)
displayAudio1 = max7219.Matrix8x8(spiAudio1, csAudio1, 4)
displayAudio1.brightness(AudioMatrixBrightness)

spiAudio2 = SPI(0,sck=Pin(18),mosi=Pin(19))
csAudio2 = Pin(26, Pin.OUT)
displayAudio2 = max7219.Matrix8x8(spiAudio2, csAudio2, 4)
displayAudio2.brightness(AudioMatrixBrightness)


def Scroll():
    display1.fill(0)
    display1.text('Too Soon',0,0,1)
    n=0
    while n < 65:
        display1.show()
        time.sleep(0.2)
        display1.scroll(-1,0)
        n = n + 1
    

def TimeMatrix(Display,Timer):
    Display.fill(0)
    Display.text('{0:04d}'.format(Timer),0,0,1)
    Display.show()

def BlankDisplay(Display):
    Display.fill(0)
    Display.show()


VisualGameInProgress = False
AudioGameInProgress = True

TooSoon1 = True
TooSoon2 = False

TooSlow1 = False
TooSlow2 = True

#Set the scrolling speed
ScrollPause = 0.05

#Define the scrolling message
scrolling_messageSoon = "For tidlig"
scrolling_messageSlow = "For sakte"
#Get the message length

if len(scrolling_messageSoon)>len(scrolling_messageSlow):
    length = len(scrolling_messageSoon)
else:
    length = len(scrolling_messageSlow)
#Calculate number of columns of the message
column = (length * 8)
#Clear the display.


while True:
    while VisualGameInProgress == True:
        display1 = displayAudio1
        display2 = displayAudio2
                
        if TooSoon1 == True or TooSlow1 == True:   
            display1.fill(0)
            display1.show()
        
        if TooSoon2 == True or TooSlow2 == True:
            display2.fill(0)
            display2.show()
        
        time.sleep(ScrollPause)

        for x in range(32, -column, -1):     
        #Clear the display
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

            time.sleep(0.05)
        
    while AudioGameInProgress == True:
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

        for x in range(32, -column, -1):     
        #Clear the display
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
