#!/usr/bin/env python
"""
Link voicemeeter status to two blink(1) devices
- blink device #1 will show output mute status
- blink device #2 will show microphone mute status

"""

import time,sys,signal
import voicemeeter
from blink1.blink1 import Blink1
from blink1.blink1 import Blink1ConnectionFailed

def connect_to_devices(keeptrying=False):
    # Attempt to connect to a couple of specific Blink devices
    # If keeptrying is set to True, keep trying to connect indefinitely

    # Loop until we encounter a return statement or exception
    while True:
        try:
            print("Attempting to connect to Blink(1) devices...")
            # My blink serials
            # 32866fd7,3f39b147
            dev1=u'32866fd7'
            dev2=u'3f39b147'
            device1 = Blink1( serial_number=dev1 ) # first blink1
            device2 = Blink1( serial_number=dev2 ) # last blink1
            print("Connection established to Blink devices.")
            return (device1, device2)
        except:
            # One of the devices isn't connected
            if keeptrying:
                # Wait a few seconds and try again
                time.sleep(3)
            else:
                print("Specified Blink1 devices were not found. Exiting...")
                sys.exit()

# List currently connected serials
blink1_serials = Blink1.list()
if blink1_serials:
    print("blink(1) devices found: "+ ','.join(blink1_serials))
else:
    print("no blink1 found")
    sys.exit()

# Attempt to connect to devices
device1,device2 = connect_to_devices(keeptrying=True)

# Kind of Voicemeeter program
kind = 'banana'

# Make sure we can access voicemeeter successfully.. but try to avoid foregrounding it if
# we can.
try:
    vmr = voicemeeter.remote(kind)
    vmr.login()
except voicemeeter.errors.VMRDriverError:
    print("Looks like Voicemeeter isn't running... starting it up now.")
    voicemeeter.launch(kind)
    vmr.login()

print("Voicemeeter interface established.")

# Catch keyboard interrupt (Ctrl+C)
signal.signal(signal.SIGINT, signal.default_int_handler)

# Loop forever
while True:
    try:
        # Check that both B1 and B2 outputs are muted
        if vmr.outputs[3].mute and vmr.outputs[4].mute:
            # We're muted, set the green color I like
            device2.fade_to_color(0, '#0B610B')
        else:
            # We're not muted, set a nice red color
            device2.fade_to_color(0, '#8A0829')

        # Check that A1, A2, A3 are activated
        if vmr.inputs[3].A1 and vmr.inputs[3].A2 and vmr.inputs[3].A3:
            # Output is active, set it to a chill blue
            device1.fade_to_color(0, '#0431B4')
        else:
            # Output is muted
            device1.fade_to_color(0, '#B40486')
        
        # I can't stand keyboard delay so making this a really short sleep..
        time.sleep(0.02)

    except Blink1ConnectionFailed:
        print("One of the Blink devices seems to have gone missing...")
        # Attempt to reconnect to devices
        device1,device2 = connect_to_devices(keeptrying=True)

    except KeyboardInterrupt:
        print("Shutting down script...")
        device1.close()
        device2.close()
        vmr.logout()
        sys.exit()

