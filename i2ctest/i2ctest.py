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
STR    = 10



###############################################################################
# Settings

# Initialize I2C with pins
i2c = machine.I2C(0,
                 # scl=machine.Pin(21),
                 # sda=machine.Pin(20),
                  scl=machine.Pin(13),
                  sda=machine.Pin(12),
                  freq=400000)
i2c1 = machine.I2C(1,
                 # scl=machine.Pin(21),
                 # sda=machine.Pin(20),
                  sda=machine.Pin(6),
                  scl=machine.Pin(7),
                  freq=400000)

###############################################################################
# Functions
print(i2c.scan() )
print(i2c1.scan())

def reg_write(i2c, addr, reg, data):
    """
    Write bytes to the specified register.
    """
    if type(data) is bytearray:
        msg = data
    elif type(data) is str:
        msg = bytearray()
        msg.extend(data.encode())
        print(str(int(msg[0]))+" "+str(int(msg[1]))+"*"+str(msg)+"*")
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
    if side==0:
        reg_write(i2c, ADXL343_ADDR, RED+128*half, colour)
    if side==1:
        reg_write(i2c1, ADXL343_ADDR, RED+128*half, colour)

def sendText(side, half, colour, mode, text, scrollspeed=2):
    if side==0:
        reg_write(i2c, ADXL343_ADDR, RED+128*half, colour)
        reg_write(i2c, ADXL343_ADDR, STRLEN, len(text))
        reg_write(i2c, ADXL343_ADDR, STR, text)
        reg_write(i2c, ADXL343_ADDR, MODE, mode)
        reg_write(i2c, ADXL343_ADDR, SCROLLSPEED, scrollspeed)
        reg_write(i2c, ADXL343_ADDR, SCROLLPOS,0)
    elif side==1:
        reg_write(i2c1, ADXL343_ADDR, RED+128*half, colour)
        reg_write(i2c1, ADXL343_ADDR, STRLEN, len(text))
        reg_write(i2c1, ADXL343_ADDR, STR, text)
        reg_write(i2c1, ADXL343_ADDR, MODE, mode)
        reg_write(i2c1, ADXL343_ADDR, SCROLLSPEED, scrollspeed)
        reg_write(i2c1, ADXL343_ADDR, SCROLLPOS,0)
        
def sendTraffic(side, half, colour, radius=7):
    if side==0:
        reg_write(i2c, ADXL343_ADDR, RED+128*half, colour)
        reg_write(i2c, ADXL343_ADDR, RADIUS+128*half, radius)
        reg_write(i2c, ADXL343_ADDR, MODE+128*half, MODE_TRAFFIC)
    elif side==1:
        reg_write(i2c1, ADXL343_ADDR, RED+128*half, colour)
        reg_write(i2c1, ADXL343_ADDR, RADIUS+128*half, radius)
        reg_write(i2c1, ADXL343_ADDR, MODE+128*half, MODE_TRAFFIC)
        
def sendClear(side, half):
    if side==0:
        reg_write(i2c, ADXL343_ADDR, MODE+128*half, MODE_BLANK)
    elif side==1:
        reg_write(i2c1, ADXL343_ADDR, MODE+128*half, MODE_BLANK)
        
sendClear(0,0)
sendClear(0,1)
# Read device ID to make sure that we can communicate with the ADXL343
#data = reg_read(i2c, ADXL343_ADDR, 10)
#print(data)
#print(reg_write(i2c, ADXL343_ADDR, RED, bytearray([255,50,50])))
#print(reg_write(i2c, ADXL343_ADDR, STR, "Hello world how are you"))
sendText(0, 0, [0,0,255], MODE_SCROLL, "Hello world how are you", scrollspeed=1)
#print(reg_write(i2c, ADXL343_ADDR, STRLEN, 23))
#print(reg_write(i2c, ADXL343_ADDR, MODE, MODE_SCROLL))
#print(reg_write(i2c, ADXL343_ADDR, SCROLLSPEED, 1))
#print(reg_write(i2c, ADXL343_ADDR, SCROLLPOS, 0))
data = reg_read(i2c, ADXL343_ADDR, RED,3)
print(data)
data = reg_read(i2c, ADXL343_ADDR, STR,5)
print(data)



# Wait before taking measurements
utime.sleep(2.0)
sendTraffic(1, 1, [255,0,0], radius=7)
#print(reg_write(i2c, ADXL343_ADDR, 128+RED, [255,0,0]))
#print(reg_write(i2c, ADXL343_ADDR, 128+RADIUS, 7))
#print(reg_write(i2c, ADXL343_ADDR, 128+MODE, MODE_TRAFFIC))
utime.sleep(2.0)
sendTraffic(1, 1, [128,128,0], radius=7)
#print(reg_write(i2c, ADXL343_ADDR, 128+RED, [255,255,0]))
utime.sleep(2.0)
sendTraffic(1, 1, [0,255,0], radius=8)
#print(reg_write(i2c, ADXL343_ADDR, 128+RED, [0,255,0]))
#print(reg_write(i2c, ADXL343_ADDR, 128+RADIUS, 8))
