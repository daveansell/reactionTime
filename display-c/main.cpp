#include "libraries/pico_graphics/pico_graphics.hpp"
#include "libraries/interstate75/interstate75.hpp"
#include "drivers/rgbled/rgbled.hpp"
#include "drivers/button/button.hpp"

//#include "pico_i2c_slave/include/pico/i2c_fifo.h"
#include "pico_i2c_slave/include/pico/i2c_slave.h"


#include <pico/stdlib.h>
#include <stdio.h>
#include <string.h>
//#include <pico/i2c_slave.h>

// Modes
const uint8_t MODE_BLANK   = 0;
const uint8_t MODE_LTEXT    = 1;
const uint8_t MODE_RTEXT    = 2;
const uint8_t MODE_SCROLL  = 3;
const uint8_t MODE_TRAFFIC = 4;

// Registers
const uint8_t MODE = 2;
const uint8_t RED = 3;
const uint8_t GREEN = 4;
const uint8_t BLUE = 5;
const uint8_t RADIUS = 6;
const uint8_t SCROLLPOS = 7;
const uint8_t SCROLLSPEED = 8;
const uint8_t STRLEN = 9;
const uint8_t SIZE = 10;
const uint8_t STR = 11;

uint8_t halves[] = { 0, 127 };
int32_t offsets[] = { 0,0};

static const uint I2C_SLAVE_ADDRESS = 0x17;
static const uint I2C_BAUDRATE = 100000; // 100 kHz

// For this example, we run both the master and slave from the same board.
// You'll need to wire pin GP4 to GP6 (SDA), and pin GP5 to GP7 (SCL).
static const uint I2C_SLAVE_SDA_PIN = 20;
static const uint I2C_SLAVE_SCL_PIN = 21;

// The slave implements a 256 byte memory. To write a series of bytes, the master first
// writes the memory address, followed by the data. The address is automatically incremented
// for each byte transferred, looping back to 0 upon reaching the end. Reading is done
// sequentially from the current memory address.
static struct
{
    int8_t mem[256];
    uint8_t mem_address;
    bool mem_address_written;
} context;


static void i2c_slave_handler(i2c_inst_t *i2c, i2c_slave_event_t event) {
    switch (event) {
    case I2C_SLAVE_RECEIVE: // master has written some data
        if (!context.mem_address_written) {
            // writes always start with the memory address
            context.mem_address = i2c_read_byte_raw(i2c);
            context.mem_address_written = true;
        } else {
            // save into memory
            context.mem[context.mem_address] = i2c_read_byte_raw(i2c);
            context.mem_address++;
        }
        break;
    case I2C_SLAVE_REQUEST: // master is requesting data
        // load from memory
        i2c_write_byte_raw(i2c, context.mem[context.mem_address]);
        context.mem_address++;
        break;
    case I2C_SLAVE_FINISH: // master has signalled Stop / Restart
        context.mem_address_written = false;
        break;
    default:
        break;
    }
}
static void setup_slave() {

    gpio_init(I2C_SLAVE_SDA_PIN);
    gpio_set_function(I2C_SLAVE_SDA_PIN, GPIO_FUNC_I2C);
    gpio_pull_up(I2C_SLAVE_SDA_PIN);

    gpio_init(I2C_SLAVE_SCL_PIN);
    gpio_set_function(I2C_SLAVE_SCL_PIN, GPIO_FUNC_I2C);
    gpio_pull_up(I2C_SLAVE_SCL_PIN);

    i2c_init(i2c0, I2C_BAUDRATE);
    // configure I2C0 for slave mode
    i2c_slave_init(i2c0, I2C_SLAVE_ADDRESS, &i2c_slave_handler);
}



using namespace pimoroni;
// Display driver for a single 32x32 hub75 matrix
Hub75 hub75(32, 32, nullptr, PANEL_FM6126A, false);

// Graphics library - in 24Bit mode with 16M colours
PicoGraphics_PenRGB888 graphics(hub75.width, hub75.height, nullptr);

// And each button
Button button_a(Interstate75::A);
// For the Interstate75
// Button button_b(Interstate75::BOOT); // Using this button definition on the Interstate75W will most likely disable the wifi make sure it is commented out if using Interstate75W

// Or for the Interstate75W
Button button_b(Interstate75::B); // This button is not present on the Interstate75 (non W version)
// RGB LED
RGBLED led(Interstate75::LED_R, Interstate75::LED_G, Interstate75::LED_B, ACTIVE_LOW);

// Interrupt callback required function 
void __isr dma_complete() {
  hub75.dma_complete();
}

int main() {
    stdio_init_all();
    setup_slave();
    hub75.start(dma_complete);
    led.set_rgb(0,0,0);
    char strings[2][128];
    strcpy(strings[0],"Hello");
    strcpy(strings[1],"World");
    int txtWidth = 0;
    int32_t scrollCounter[] = {0,0};
    context.mem[SIZE] = 96;
    context.mem[SIZE+128] = 96;
    while(true) {
	for(uint8_t i=0; i<2; i++){
		int o = 128 * i;
		int y = 16  * i;
//		memcpy(strings[i], (void*)context.mem[o+STR], context.mem[o+STRLEN]);
		for(int p =0; p<context.mem[o+STRLEN]; p++){
			strings[i][p]=context.mem[o+STR+p];
		}
		strings[i][context.mem[o+STRLEN]] = '\0';	
    //		std::basic_string_view<int8_t> sv(strings[i], context.mem[o+STRLEN]) ;
        	graphics.set_pen(0, 0, 0);
        	Rect text_rect(0, y, hub75.width, hub75.height/2);
        	graphics.rectangle(text_rect);
		if( i==0){
			printf("Hello, %d %d-> %d %d %s %d->%d-%d\n",(int)context.mem[o+STR],(int)context.mem[o+STR+1], (int)strings[i][0], (int)strings[i][1], strings[i], offsets[i], scrollCounter[i], -txtWidth*2+hub75.width+(offsets[i]+hub75.width-txtWidth)%(hub75.width+txtWidth*2));
		}
		float textSize = (float)context.mem[o+SIZE] /64.0 ;
		switch(context.mem[o+MODE]){
			case MODE_BLANK:
				break;
			case MODE_LTEXT:
        			graphics.set_pen(context.mem[o+RED], context.mem[o+GREEN], context.mem[o+BLUE]);
        			graphics.text(strings[i], Point(text_rect.x, y), text_rect.w, textSize );
				break;
			case MODE_RTEXT:
        			graphics.set_pen(context.mem[o+RED], context.mem[o+GREEN], context.mem[o+BLUE]);
				txtWidth = graphics.measure_text(strings[i], textSize);
        			graphics.text(strings[i], Point(hub75.width - txtWidth, y), text_rect.w, textSize);
				break;
			case MODE_SCROLL:
				txtWidth = graphics.measure_text(strings[i], textSize);
				graphics.set_pen(context.mem[o+RED], context.mem[o+GREEN], context.mem[o+BLUE]);
				graphics.text(strings[i], Point(-txtWidth+(offsets[i]+hub75.width+txtWidth), y), 2000, textSize);
//offsets[i] ++;
				if(offsets[i] < - (hub75.width+txtWidth)){
					offsets[i]=0;
				}
				break;
			case MODE_TRAFFIC:
				graphics.set_pen(context.mem[o+RED], context.mem[o+GREEN], context.mem[o+BLUE]);
				graphics.circle(Point((hub75.width/2), 7+y), context.mem[o+RADIUS]);
				

		}
        	hub75.update(&graphics);
		if (scrollCounter[i]> ((uint32_t) context.mem[o+SCROLLSPEED])*10 ){
			offsets[i]-=1;
			scrollCounter[i]=0;
			printf("offset %d-%d-%d ", scrollCounter[i], ((uint32_t) context.mem[o+SCROLLSPEED])*10);
		}
		if (context.mem[o+SCROLLPOS]!=-127){
			offsets[i]=context.mem[o+SCROLLPOS];
			context.mem[o+SCROLLPOS]=-127;
			printf("QQ %d", context.mem[o+SCROLLPOS]);
		}
		scrollCounter[i]++;

	}

        // now we've done our drawing let's update the screen
    }
}

