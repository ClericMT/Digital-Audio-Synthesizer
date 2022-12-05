import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

import liblo as OSC
import sys

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan4 = AnalogIn(mcp, MCP.P4)
chan2 = AnalogIn(mcp, MCP.P2)

#####

# send all messages to port 1234 on the local machine
try:
    target = OSC.Address(1234)
except OSC.AddressError as err:
    print(err)    
    sys.exit()

# start the transport via OSC
OSC.send(target, "/rnbo/jack/transport/rolling", 1)

while True:
    pot_1 = chan4.value / 256
    pot_2 = chan2.value / 256
    print(pot_1)
    print(pot_2)
    OSC.send(target, "/rnbo/inst/0/params/time", pot_1)
    OSC.send(target, "/rnbo/inst/0/params/color", pot_2)