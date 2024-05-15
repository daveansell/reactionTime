# Example using PIO to create a UART RX interface.
#
# To make it work you'll need a wire connecting GPIO4 and GPIO3.
#
# Demonstrates:
#   - PIO shifting in data on a pin
#   - PIO jmp(pin) instruction
#   - PIO irq handler
#   - using the second core via _thread

# ruff: noqa: F821 - @asm_pio decorator adds names to function scope
import _thread
from machine import Pin, UART
from rp2 import PIO, StateMachine, asm_pio
import time
import interstate75
i75 = interstate75.Interstate75(display=interstate75.DISPLAY_INTERSTATE75_32X32,  panel_type=interstate75.Interstate75.PANEL_FM6126A)
graphics = i75.display

width = i75.width
height = i75.height
devs = 1.0 / height
UART_BAUD = 9600

text = ['', '']
mode = ['', '']
colours = ["R", "G"]

#HARD_UART_TX_PIN = Pin(4, Pin.OUT)
PIO_RX_PIN = Pin(20, Pin.IN, Pin.PULL_UP)

INT_PIN = Pin(19, Pin.IN)
animate = True
stripe_width = 1.0
speed = 5.0
offset = 0.0

phase = 0
MAGENTA = graphics.create_pen(255, 0, 255)
BLACK = graphics.create_pen(0, 0, 0)
WHITE = graphics.create_pen(255, 255, 255)
RED = graphics.create_pen(255, 0, 0)
AMBER = graphics.create_pen(150, 130, 0)
GREEN = graphics.create_pen(0, 255, 0)
BLUE = graphics.create_pen(0,0,255)

ys = [3,19]

o=[0,0]
@micropython.native  # noqa: F821
def draw(offset):
    for x in range(width):
        graphics.set_pen(graphics.create_pen_hsv(devs * x + offset, 1.0, 0.5))
        for y in range(height):

            graphics.pixel(x, y)

    i75.update(graphics)


@asm_pio(
    autopush=True,
    push_thresh=8,
    in_shiftdir=rp2.PIO.SHIFT_RIGHT,
    fifo_join=PIO.JOIN_RX,
)
def uart_rx_mini():
    # fmt: off
    # Wait for start bit
    wait(0, pin, 0)
    # Preload bit counter, delay until eye of first data bit
    set(x, 7)                 [10]
    # Loop 8 times
    label("bitloop")
    # Sample data
    in_(pins, 1)
    # Each iteration is 8 cycles
    jmp(x_dec, "bitloop")     [6]
    # fmt: on


@asm_pio(
    in_shiftdir=rp2.PIO.SHIFT_RIGHT,
)
def uart_rx():
    # fmt: off
    label("start")
    # Stall until start bit is asserted
    wait(0, pin, 0)
    # Preload bit counter, then delay until halfway through
    # the first data bit (12 cycles incl wait, set).
    set(x, 7)                 [10]
    label("bitloop")
    # Shift data bit into ISR
    in_(pins, 1)
    # Loop 8 times, each loop iteration is 8 cycles
    jmp(x_dec, "bitloop")     [6]
    # Check stop bit (should be high)
    jmp(pin, "good_stop")
    # Either a framing error or a break. Set a sticky flag
    # and wait for line to return to idle state.
    irq(block, 4)
    wait(1, pin, 0)
    # Don't push data if we didn't see good framing.
    jmp("start")
    # No delay before returning to start; a little slack is
    # important in case the TX clock is slightly too fast.
    label("good_stop")
    push(block)
    # fmt: on


# The handler for a UART break detected by the PIO.
def handler(sm):
    print("break", time.ticks_ms(), end=" ")


# Function for core1 to execute to write to the given UART.
#def core1_task(uart, text):
 #   uart.write(text)
def handleCmd(buf):
    global text, mode,o
    parts = buf.split('-')
    if len(parts)==3:
        if parts[0]=='T':
            half = 0
        else:
            half = 1
        if parts[1] in ['T','L', 'R', 'I']:
            text[half] = parts[2]
            mode[half] = parts[1]
        elif parts[1] == 'C':
            if parts[2] in ['R', 'G', 'Y', 'P', 'W', 'L', 'B']:
                colours[half] = parts[2]
        o[half]=32

def getColour(colour):
    if colour=='R':
        return RED
    if colour == 'G':
        return GREEN
    if colour == 'Y':
        return AMBER
    if colour == 'W':
        return WHITE
    if colour == 'L':
        return BLACK
    if colour == 'B':
        return BLUE
    
# Set up the hard UART we're going to use to print characters.
#uart = UART(1, UART_BAUD, tx=HARD_UART_TX_PIN)
def readSerial():
 #   for pio_prog in ("uart_rx"):#_mini", "uart_rx"):
    # Set up the state machine we're going to use to receive the characters.
        sm = StateMachine(
            3,
            globals()["uart_rx"],
            freq=8 * UART_BAUD,
            in_base=PIO_RX_PIN,  # For WAIT, IN
            jmp_pin=PIO_RX_PIN,  # For JMP
        )
        sm.irq(handler)
        sm.active(1)

        buf = ''
        while 1:#sm.rx_fifo()>0:
            b = sm.get() >> 24
            c = chr(b)
            #print(c+" "+str(b))
            if b == 10:
                print(buf)
                handleCmd(buf)
                buf=''
                
            else:
                buf += c
            #print(chr(sm.get() >> 24), end="")
    # Tell core 1 to print some text to UART 1
#    text = "Hello, world from PIO, using {}!".format(pio_prog)
 #   _thread.start_new_thread(core1_task, (uart, text))
second_thread = _thread.start_new_thread(readSerial, ())
    # Echo characters received from PIO to the console.

while 1:
#        if  animate:
 #           phase += speed

  #          start = time.ticks_ms()
   #         offset += 0.05
            
    #        draw(offset)
    graphics.set_pen(BLACK)
    graphics.clear()
    graphics.set_font("bitmap8")
    
    for i in range(0,2):
        if mode[i]=='T':
            graphics.set_pen(getColour(colours[i]))
            graphics.text(text[0], o[i], ys[i], scale=1.5)

        elif mode[i]=='I':
            if text[i]=='G':
                graphics.set_pen(GREEN)
                r=7
            elif text[i]=="Y":
                graphics.set_pen(AMBER)
                r=6
            else:
                graphics.set_pen(RED)
                r=6
            graphics.circle(16,16*i+7,r)
        elif mode[i]=='L':
            graphics.set_pen(getColour(colours[i]))
            graphics.text(text[i], 1, ys[i], scale=1)
        elif mode[1]=='R':
            graphics.set_pen(getColour(colours[i]))
            width = graphics.measure_text(text[i], scale=1)#, spacing, fixed_width)

            graphics.text(text[i], 32-width, ys[i], scale=1)
    i75.update(graphics)
    time.sleep(0.02)
    o[0]-=1
    o[1]-=1
     #   scroll(line1)
      #  scroll(line2)
    #reverse_scroll(line2)
     #   display.refresh(minimum_frames_per_second=0)
    #print()

print("end")