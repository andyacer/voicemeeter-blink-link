#!/usr/bin/env python
"""
Link voicemeeter status to two blink(1) devices
- blink device #1 will show output mute status
- blink device #2 will show microphone mute status

# Note that the colors used by the device compared to what is shown in the blink control
# utility program are 2 shades brighter.  So if you want to use the rich pink color of
# B40486, you have to actually choose 2 colors darker (2 down in the grid), 610B4B.

"""

import time,sys,signal
import voicemeeter
from blink1.blink1 import Blink1
from blink1.blink1 import Blink1ConnectionFailed
from voicemeeter.errors import VMRDriverError

def sleep_or_quit(duration):
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        print("Shutting down script...")
        try:
            device1.fade_to_color(0, '#400000')
            device2.fade_to_color(0, '#400000')
            device1.close()
            device2.close()
            vmr.logout()
        except NameError:
            pass
        sys.exit()

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
        except KeyboardInterrupt:
            print("Shutting down script...")
            device1.close()
            device2.close()
            vmr.logout()
            sys.exit()
        except Blink1ConnectionFailed:
            # One of the devices isn't connected
            if keeptrying:
                # Wait a few seconds and try again
                sleep_or_quit(3)
            else:
                print("Specified Blink1 devices were not found. Exiting...")
                sys.exit()
            
            #print("Unexpected error:", sys.exc_info()[0])
            #raise

def login():
    #while True:
        # Make sure we can access voicemeeter successfully.. but try to avoid foregrounding it if
        # we can.
    try:
        vmr.login()
        print("Voicemeeter interface established. (Sometimes this isn't true.. not sure why..)")
    except voicemeeter.errors.VMRDriverError as err:
        print("Voicemeeter not running (or some other error), waiting for it to start...")
        # sleep_or_quit(3)
        # Some error
        print("[*] Error info: " + str(err))
        # Could launch it like this..
        #voicemeeter.launch(kind)

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
kind = 'potato'

# Setup VMR object
vmr = voicemeeter.remote(kind)

# Catch keyboard interrupt (Ctrl+C)
signal.signal(signal.SIGINT, signal.default_int_handler)

# Loop forever
while True:
    try:
        # Debugging
        #import pdb; pdb.set_trace()
        # Check that both B1 and B2 outputs are muted
        if vmr.outputs[5].mute and vmr.outputs[6].mute and vmr.outputs[7].mute:
            # We're muted, set the green color I like
            # These colors are off by 2 rows of brightness it seems.
            # Blink setting: 04B404 ... API setting => 0B610B
            # Blink setting: 088A08 ... API setting => 0B3B0B
            device2.fade_to_color(0, '#0B3B0B')
        else:
            # We're not muted, set a nice red color
            # Previous: 8A0829
            # Darker color: 610B21
            device2.fade_to_color(0, '#610B21')

        # Check that A1, A2, A3 are activated
        if vmr.inputs[5].A1 and vmr.inputs[5].A2 and vmr.inputs[5].A3\
            and vmr.inputs[5].A4 and vmr.inputs[5].A5:
            # Output is active, set it to a chill blue. Orig: 0431B4, darker: 0B2161
            device1.fade_to_color(0, '#0B2161')
        else:
            # Output is muted - bright pink
            # Previous: B40486
            # Darker: 610B4B
            device1.fade_to_color(0, '#610B4B')
        
        # I can't stand keyboard delay so making this a really short sleep..
        sleep_or_quit(0.02)

    except Blink1ConnectionFailed:
        print("One of the Blink devices seems to have gone missing...")
        # Attempt to reconnect to devices
        device1,device2 = connect_to_devices(keeptrying=True)

    except VMRDriverError as err:
        # Attempt to reconnect to login to voicemeeter
        #print("Error info before calling login:\n" + str(err))
        login()
        device1.fade_to_color(0, '#400000')
        device2.fade_to_color(0, '#400000')
        sleep_or_quit(2)

    except KeyboardInterrupt:
        print("Shutting down script...")
        device1.close()
        device2.close()
        vmr.logout()
        sys.exit()
