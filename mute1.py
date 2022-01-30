# Get the mididings and OSC stuffs
from mididings import *
from mididings.extra.osc import SendOSC

# Set up the OSC port 
#(you define it in non-mixer thanks to  "--osc-port=7587" option - no quotes)
port = 7587

SendOSC(port, '/strip/Distortion%20Output/Gain/Mute', lambda ev: ev.value / 127.0)

