from machine import UART, Pin
import time
uarts = [
    UART(0, baudrate=9600, tx=Pin(012), rx=Pin(13)),
    UART(1, baudrate=9600, tx=Pin(08), rx=Pin(9))
    ]

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
    print(str(half)+"-C-"+str(colour))
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
    print(str(half)+"-"+str(mode)+"-"+str(text))
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
    
    
while 1:
    setDisplayColour(0, "T", "B")
    setDisplayText(0, "T", "T", "we should have text")
    time.sleep(3)
    setDisplayColour(0, "B", "R")
    setDisplayText(0, "B", "L", "boo")
    time.sleep(1)
    setTrafficLight(1,"B","R")
    time.sleep(1)
    setTrafficLight(0,"B","Y")
    time.sleep(1)
    setTrafficLight(0,"T","G")
    setTrafficLight(0,"B","G")
    setDisplayText(0, "T", "S", "Croll")
    time.sleep(2)
        
    setTrafficLight(1,"T","G")
    time.sleep(1)
    setTrafficLight(1,"B","R")
    time.sleep(1)
            
    setDisplayText(1,"B","L","beep")
    time.sleep(1)
    setDisplayText(1,"T","R","45")
    
    setDisplayText(1, "T", "S", "Scrolling")
    time.sleep(1)
    """uart.write("B-I-Y\n")time.sleep(1)
    time.sleep(1.5)
    uart.write("B-I-G\n")
    time.sleep(2)
    uart.write("B-R-354.6\n")
    time.sleep(2)
    uart.write("T-C-W\n")
    uart.write("T-L-34\n")
    time.sleep(2)
    
"""