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
btn = digitalio.DigitalInOut(board.D2)
btn.direction = digitalio.Direction.INPUT

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)
chan1 = AnalogIn(mcp, MCP.P1)
chan2 = AnalogIn(mcp, MCP.P2)
chan3 = AnalogIn(mcp, MCP.P3)

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
    pot_0 = chan0.value / 256 / 2.56
    pot_1 = chan1.value / 256 / 2.56
    pot_2 = chan2.value / 256 / 2.56
    pot_3 = chan3.value / 256 / 2.56
    print(pot_0)
    print(pot_1)
    print(pot_2)
    print(pot_3)
    print(btn.value)
    OSC.send(target, "/rnbo/inst/0/params/pot_one", float(pot_0))
    OSC.send(target, "/rnbo/inst/0/params/pot_two", float(pot_1))
    OSC.send(target, "/rnbo/inst/0/params/pot_three", float(pot_2))
    OSC.send(target, "/rnbo/inst/0/params/pot_four", float(pot_3))
    OSC.send(target, "/rnbo/inst/0/params/btn", float(btn.value))
