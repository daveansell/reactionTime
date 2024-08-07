import machine
import utime
import ustruct
import sys

###############################################################################
# Constants

# I2C address
ADXL343_ADDR = 0x17
#// Modes
MODE_BLANK    = 0
MODE_LTEXT    = 1
MODE_RTEXT    = 2
MODE_SCROLL   = 3
MODE_TRAFFIC  = 4

#// Registers
MODE   = 2
RED    = 3
GREEN  = 4
BLUE   = 5
RADIUS = 6
SCROLLPOS = 7
SCROLLSPEED = 8
STRLEN = 9
SIZE   = 10
STR    = 11

C_RED=[255,0,0]
C_YELLOW = [180,180,0]
C_GREEN = [0,255,0]
C_BLUE = [0,0,200]
C_WHITE = [255,255,255]
C_BLACK = [0,0,0]


###############################################################################
# Settings

# Initialize I2C with pins
i2c = machine.I2C(0,
                 # scl=machine.Pin(21),
                 # sda=machine.Pin(20),
                  scl=machine.Pin(13),
                  sda=machine.Pin(12),
                  freq=50000)
i2c1 = machine.I2C(1,
                 # scl=machine.Pin(21),
                 # sda=machine.Pin(20),
                  sda=machine.Pin(6),
                  scl=machine.Pin(7),
                  freq=50000)

###############################################################################
# Functions
#print(i2c.scan() )
#print(i2c1.scan())

def reg_write(i2c, addr, reg, data):
    """
    Write bytes to the specified register.
    """
    if type(data) is bytearray:
        msg = data
    elif type(data) is str:
        msg = bytearray()
        msg.extend(data.encode())
      #  print(str(reg)+" -- "+str(int(msg[0]))+" "+str(int(msg[1]))+"*"+str(msg)+"*")
    elif type(data) is list:
        msg=bytearray(data)
    else:
    # Construct message
        msg = bytearray()
        msg.append(data)
    
    # Write out message to register
    i2c.writeto_mem(addr, reg, msg)
    
def reg_read(i2c, addr, reg, nbytes=1):
    """
    Read byte(s) from specified register. If nbytes > 1, read from consecutive
    registers.
    """
    
    # Check to make sure caller is asking for 1 or more bytes
    if nbytes < 1:
        return bytearray()
    
    # Request data from specified register(s) over I2C
    data = i2c.readfrom_mem(addr, reg, nbytes)
    
    return data

###############################################################################
# Main

def setColour(side, half, colour):
    if len(colour) != 3:
        print("should have 3 parts of a colour have "+str(colour))
        return
    if side==1:
        reg_write(i2c, ADXL343_ADDR, RED+128*half, colour)
    if side==2:
        reg_write(i2c1, ADXL343_ADDR, RED+128*half, colour)

def readColour(side, half):
    if side==1:
        return reg_read(i2c, ADXL343_ADDR, RED+128*half, 3)
    else:
        return reg_read(i2c1, ADXL343_ADDR, RED+128*half, 3)
def sendText(side, half, colour, mode, text, scrollspeed=2, size = 1.5):
    #print(readColour(side,half))
    iSize = max(min(int(size * 64 ), 255),0)
    if len(colour) != 3:
        print("should have 3 parts of a colour have "+str(colour))
        return
    print("side="+str(side)+" half="+str(half)+" colour="+str(colour)+" mode="+str(mode)+" text="+str(text))
    if side==1:
        reg_write(i2c, ADXL343_ADDR, RED+128*half, colour)
        reg_write(i2c, ADXL343_ADDR, SIZE+128*half, iSize)
        reg_write(i2c, ADXL343_ADDR, STRLEN+128*half, len(text))
        if len(text):
            reg_write(i2c, ADXL343_ADDR, STR+128*half, text)
        reg_write(i2c, ADXL343_ADDR, MODE+128*half, mode)
        reg_write(i2c, ADXL343_ADDR, SCROLLSPEED+128*half, scrollspeed)
        reg_write(i2c, ADXL343_ADDR, SCROLLPOS+128*half,0)
    elif side==2:
        reg_write(i2c1, ADXL343_ADDR, RED+128*half, colour)
        reg_write(i2c1, ADXL343_ADDR, SIZE+128*half, iSize)
        reg_write(i2c1, ADXL343_ADDR, STRLEN+128*half, len(text))
        if len(text):
            reg_write(i2c1, ADXL343_ADDR, STR+128*half, text)
        reg_write(i2c1, ADXL343_ADDR, MODE+128*half, mode)
        reg_write(i2c1, ADXL343_ADDR, SCROLLSPEED+128*half, scrollspeed)
        reg_write(i2c1, ADXL343_ADDR, SCROLLPOS+128*half,0)
        
def sendTraffic(side, half, colour, radius=7):
    if len(colour) != 3:
        print("should have 3 parts of a colour have "+str(colour))
        return
    if side==1:
        reg_write(i2c, ADXL343_ADDR, RED+128*half, colour)
        reg_write(i2c, ADXL343_ADDR, RADIUS+128*half, radius)
        reg_write(i2c, ADXL343_ADDR, MODE+128*half, MODE_TRAFFIC)
    elif side==2:
        reg_write(i2c1, ADXL343_ADDR, RED+128*half, colour)
        reg_write(i2c1, ADXL343_ADDR, RADIUS+128*half, radius)
        reg_write(i2c1, ADXL343_ADDR, MODE+128*half, MODE_TRAFFIC)
        
def sendClear(side, half):
    if side==1:
        reg_write(i2c, ADXL343_ADDR, MODE+128*half, MODE_BLANK)
    elif side==2:
        reg_write(i2c1, ADXL343_ADDR, MODE+128*half, MODE_BLANK)

