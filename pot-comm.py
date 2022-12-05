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
chan = AnalogIn(mcp, MCP.P0)

print("Raw ADC Value: ", chan.value)
print("ADC Voltage: " + str(chan.voltage) + "V")

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
    pot_1 = chan.value
    print(pot_1)
    OSC.send(target, "/rnbo/inst/0/params/frequency", pot_1)