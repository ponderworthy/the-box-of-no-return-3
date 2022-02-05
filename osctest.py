# Get the mididings and OSC stuffs
from mididings import *
from mididings.extra.osc import SendOSC

# Set up the OSC port 
#(you define it in non-mixer thanks to  "--osc-port=7587" option - no quotes)
port = 7587
 
#The actual conversion stuff
run(
   Filter(CTRL) >> CtrlSplit({
       # Non-mixer maping
       #It's always : /strip/[strip_name]/[effect_name]/[control_name]
       #Non-mixer uses values from 0.0 to 1.0. Therfore you have to divide by 127
       # Caution : 127.0 ( .0 !!). Check 'python's promotion' if you want to know why.

       #Sending MIDI CC #16 to the pan pot of the "mix1" strip
       # 16: SendOSC(port, '/strip/DistortionOutput/Mono%20Pan/Pan', lambda ev: ev.value / 127.0),
       # 17: SendOSC(port, '/strip/mix2/Mono%20Pan/Pan', lambda ev: ev.value / 127.0),

       # CC0 is sent to the gain of the "mix1" strip
       0: SendOSC(port, '/strip/DistortionOutput/Gain/Gain%20(dB)', lambda ev: ev.value / 127.0),
       # 1: SendOSC(port, '/strip/mix2/Gain/Gain%20(dB)', lambda ev: ev.value / 127.0),
   })
)

