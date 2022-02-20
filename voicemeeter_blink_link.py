#!/usr/bin/env python
"""
Link voicemeeter status to two blink(1) devices
- blink device #1 will show output mute status
- blink device #2 will show microphone mute status

"""

import time,sys,signal
import voicemeeter
from blink1.blink1 import Blink1

blink1_serials = Blink1.list()
if blink1_serials:
    print("blink(1) devices found: "+ ','.join(blink1_serials))
else:
    print("no blink1 found")
    sys.exit()

# My blink serials
# 32866fd7,3f39b147
dev1=u'32866fd7'
dev2=u'3f39b147'

print("Opening first blink(1)")
blink1 = Blink1( serial_number=dev1 ) # first blink1

print("Opening second blink(1)")
blink2 = Blink1( serial_number=dev2 ) # last blink1

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

print("Voicemeeter interface established.")

# Catch keyboard interrupt (Ctrl+C)
signal.signal(signal.SIGINT, signal.default_int_handler)

# Loop forever
while True:
    try:
        # Check that both B1 and B2 outputs are muted
        if vmr.outputs[3].mute and vmr.outputs[4].mute:
            # We're muted, set the green color I like
            blink2.fade_to_color(0, '#0B610B')
        else:
            # We're not muted, set a nice red color
            blink2.fade_to_color(0, '#8A0829')

        # Check that A1, A2, A3 are activated
        if vmr.inputs[3].A1 and vmr.inputs[3].A2 and vmr.inputs[3].A3:
            # Output is active, set it to a chill blue
            blink1.fade_to_color(0, '#0431B4')
        else:
            # Output is muted
            blink1.fade_to_color(0, 'pink')

        # I can't stand keyboard delay so making this a really short sleep..
        time.sleep(0.02)
    except KeyboardInterrupt:
        print("Shutting down script...")
        blink1.close()
        blink2.close()
        vmr.logout()
        sys.exit()

# Brighter red color
# blink1.fade_to_color(0, '#B40431')
# time.sleep(2)

# Catchall error handling that I won't use:
#except BaseException as err:
    #print("Some unknown error ocurred.")
    #print(f"Unexpected {err=}, {type(err)=}")
    #raise
    #sys.exit("An unhandled exception came up!")
