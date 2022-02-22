# Voicemeeter and Blink linked
This is a Python script that links a couple of ThingM Blink(1) devices to Voicemeeter status.  Here's a demo video.

https://user-images.githubusercontent.com/25163515/154858933-18b70cc5-0236-45dd-a144-afb4ed22fe23.mp4

With this script, the lights now show a constant status of whether or not the microphone is muted and whether or not the speakers are muted.  The video demonstrates that the lights show the correct status whether Voicemeeter was muted using keyboard buttons or by clicking in the graphical user interface.

Some use cases include:
* When making video recordings, you can be sure that your micrphone is live without having to check Voicemeeter directly
* Adding confidence to Zoom calls where you can be sure that your micrphone is muted when you want it to be
* In a setup involving multiple PCs and Zoom, you can control your audio without having to switch the keyboard back to the PC that's connected to the Zoom call

It uses these Python libraries: \
https://github.com/chvolkmann/voicemeeter-remote-python \
https://github.com/todbot/blink1-python

Voicemeeter Links \
https://vb-audio.com/Voicemeeter/ \
[Voicemeeter C API PDF Download](https://download.vb-audio.com/Download_CABLE/VoicemeeterRemoteAPI.pdf) \
[Voicemeeter macro buttons](https://forum.vb-audio.com/viewtopic.php?t=353) 

ThingM Blink(1) devices on Amazon \
https://www.amazon.com/ThingM-Blink-USB-RGB-BLINK1MK3/dp/B07Q8944QK

Tiny 4-key keyboard \
Amazon link: https://www.amazon.com/gp/product/B096Z5BR5L/ \
Open source keyboard configurator: https://github.com/TabbycatPie/CustomKeyboard 

