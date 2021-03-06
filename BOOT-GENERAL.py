#!/usr/bin/python3

####################################################################
# BOOT-GENERAL
#
# This is called by BOOT-INITIAL.
#
# It is not clear how much of the below remains given the migration
# to PipeWire.  The text is kept for now.
#
# JACK clients cannot be simply started
# all at once, there is relationship
# and interaction which has to be respected
# between each of them and their JACK server.
# jpctrl, a Python library for Jack Process Control,
# handles this, and thus this file is a Python3
# script.
####################################################################

import sys
import os
import jack
import jpctrl  # our own Jack Process Control

from os.path import expanduser
bnr_dir = expanduser("~") + '/BNR/'

# Detect debug mode.  On with any command-line argument.
# In debug mode, Yoshimi is run with GUI enabled, else with GUI disabled.
cmdargcount = len(sys.argv)
if cmdargcount == 2:
    # Use debug mode
    print('BOOT-GENERAL initiated.')
    print('Debug mode on!')
    debugmode = 1
else:
    # Debug mode off
    print('BOOT-GENERAL initiated.')
    print('Running normally, debug mode off.')
    debugmode = 0

# Set different PIO checks for debug mode.
if debugmode:
    yoshimi_debug_param = ''
else:
    yoshimi_debug_param = '-i'

print('-----------------------------------------------------------------')
print('Start Calf reverb for general use...')
print('-----------------------------------------------------------------')

print('\n')
if not jpctrl.spawn_and_settle('calfjackhost --client BNR-STD-Reverb reverb:SRO4PLUS'):
    jpctrl.exit_with_beep()
print('\n')

print('-----------------------------------------------------------------')
print('Pause to settle, before we run Distribute...')
print('-----------------------------------------------------------------')

# Pause was necessary under JACK for unknown reasons.  
# We'll see, under PipeWire.
# jpctrl.stdsleep(3)

print('-----------------------------------------------------------------')
print('Start Distribute.py...')
print('-----------------------------------------------------------------')

# spawn_and_settle is / was not sufficient for Distribute;
# it was necessary to wait for the JACK port to be created.
# Testing now in pipewire.

print('\nStarting Distribute.py...')

if not jpctrl.spawn_and_settle(bnr_dir + 'Distribute.py'):
    jpctrl.exit_with_beep()

if jpctrl.wait_for_jackport('Distribute.py:SRO'):
    print('Distribute.py confirmed via port SRO creation.')
else:
    print('wait_for_jackport on Distribute.py failed.')
    jpctrl.exit_with_beep()

print('-----------------------------------------------------------------')
print('Start non-mixer...')
print('-----------------------------------------------------------------')

if not jpctrl.spawn_and_settle(
        'non-mixer --instance Mixer-General ' + bnr_dir + 'non-mixer/Mixer-General --osc-port=7587'):
    jpctrl.exit_with_beep()

# if not jpctrl.wait_for_jackport('Mixer-General/CleanOutput:out-1'):
#    print('wait_for_jackport on Mixer-General failed.')
#    jpctrl.exit_with_beep()
# else:
#    print('Mixer-General ports confirmed.')

print('-----------------------------------------------------------------')
print('Start components for patch SRO...')
print('-----------------------------------------------------------------')

print('\nStart Yoshimi SRO 1...')
if not jpctrl.spawn_and_settle(
        'yoshimi ' + yoshimi_debug_param + ' -c -I -N YoshSRO1 -l ' + bnr_dir + 'YOSHIMI/SROpart1.xmz'
	):
    jpctrl.exit_with_beep()

print('\nStart Yoshimi SRO 2...')
if not jpctrl.spawn_and_settle(
        'yoshimi ' + yoshimi_debug_param + ' -c -I -N YoshSRO2 -l ' + bnr_dir + 'YOSHIMI/SROpart2.xmz',
        ):
    jpctrl.exit_with_beep()

print('\nStart Yoshimi SRO 3...')
if not jpctrl.spawn_and_settle(
        'yoshimi ' + yoshimi_debug_param + ' -c -I -N YoshSRO3 -l ' + bnr_dir + 'YOSHIMI/SROpart3.xmz',
        ):
    jpctrl.exit_with_beep()

print('\nStart CalfSRO...')
if not jpctrl.spawn_and_settle(
        'calfjackhost --client CalfSRO eq12:SRO multibandcompressor:SRO',
        ):
    jpctrl.exit_with_beep()

print('\n')

# jpctrl.stdsleep(3)

print('-----------------------------------------------------------------')
print('Start components for patch Strings...')
print('-----------------------------------------------------------------')

print('\nStart StringsSSO...')
if not jpctrl.spawn_and_settle(
        'calfjackhost --client StringsSSO fluidsynth:StringsSSO',
        ):
    jpctrl.exit_with_beep()

print('\nStart StringsBassAdd...')
if not jpctrl.spawn_and_settle(
        'calfjackhost --client StringsBassAdd ' +
        'fluidsynth:BassoonsSustain fluidsynth:ContrabassoonSolo fluidsynth:GeneralBass',
        ):
    jpctrl.exit_with_beep()

print('\nStart MaxStringsFilters...')
if not jpctrl.spawn_and_settle(
        'calfjackhost --client MaxStringsFilters eq12:MaxStrings multibandcompressor:Strings',
        ):
    jpctrl.exit_with_beep()

print('\n')


print('-----------------------------------------------------------------')
print('Start component for patch FlowBells')
print('-----------------------------------------------------------------')

print('\nStart Yoshimi for FlowBells...')
if not jpctrl.spawn_and_settle(
        'yoshimi ' + yoshimi_debug_param + ' -c -I -N YoshFlowBells -l ' + bnr_dir + 'YOSHIMI/FlowBells.xmz',
        ):
    jpctrl.exit_with_beep()

print('-----------------------------------------------------------------')
print('Load Pipewire wiring....')
print('-----------------------------------------------------------------')

from subprocess import call
call(['python', bnr_dir + 'pw-loadwires', bnr_dir + 'BNRwires.csv'])
