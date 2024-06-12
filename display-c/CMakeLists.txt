cmake_minimum_required(VERSION 3.13.0)

# Change your executable name to something creative!
set(NAME reactionsDisplay) # <-- Name your project/executable here!

set(PICO_SDK_PATH  ~/software/pico/pico-sdk)
set(PIMORONI_PICO_PATH  ~/software/pico/pimoroni-pico)
#add_subdirectory(/home/dave/software/pico/pico_i2c_slave/i2c_slave build)

include(pico_sdk_import.cmake)
include(pimoroni_pico_import.cmake)

# Gooey boilerplate
project(${NAME} C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# Initialize the SDK
pico_sdk_init()

# Add your source files
add_executable(${NAME}
    main.cpp # <-- Add source files here!
)

# enable usb output
pico_enable_stdio_usb(${NAME} 1)

pico_add_extra_outputs(${NAME})

include_directories(pico_i2c_slave)

# Include required libraries
# This assumes `pimoroni-pico` is stored alongside your project
#include(common/pimoroni_i2c)
include(common/pimoroni_bus)
include(libraries/bitmap_fonts/bitmap_fonts)
include(libraries/hershey_fonts/hershey_fonts)
include(libraries/pico_explorer/pico_explorer)
include(drivers/hub75/hub75)
include(libraries/interstate75/interstate75)
#include(rp2_common/i2c_slave/i2c_slave)
#include(i2c_slave/i2c_slave/include)


# Don't forget to link the libraries you need!
target_link_libraries(${NAME}
	    pimoroni_bus
	    pico_explorer # <-- List libraries here!
    pico_stdlib
    pico_multicore
    #   pimoroni_common
    hardware_vreg
       hub75
       rgbled
           interstate75
	pico_i2c_slave	
    hardware_i2c
    pico_stdlib
	)

# create map/bin/hex file etc.
pico_add_extra_outputs(${NAME})

# Set up files for the release packages
install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/${NAME}.uf2
    ${CMAKE_CURRENT_LIST_DIR}/README.md
    DESTINATION .
)

set(CPACK_INCLUDE_TOPLEVEL_DIRECTORY OFF)
set(CPACK_GENERATOR "ZIP" "TGZ")
include(CPack)

get_property(dirs DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY INCLUDE_DIRECTORIES)
foreach(dir ${dirs})
  message(STATUS "dir='${dir}'")
endforeach()
pico_enable_stdio_usb(${NAME} 1)
pico_enable_stdio_uart(${NAME} 0)
