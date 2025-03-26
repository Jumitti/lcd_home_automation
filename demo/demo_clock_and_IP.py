#! /usr/bin/env python

from lcd_16x2 import drivers
from time import sleep
from datetime import datetime
from subprocess import check_output

import sys

if sys.platform != "linux":
    print("Warning: This script uses 'smbus', which is specific to Raspberry Pi.")
    print("You are on a different system (Windows, macOS, etc.). The demo will not function as expected.")
    print("Please try running this script on a Raspberry Pi for full functionality or use demo_emulator.py instead.")
    sys.exit(1)


display = drivers.Lcd()
IP = check_output(["hostname", "-I"], encoding="utf8").split()[0]
try:
    print("Writing to display")
    while True:
        display.lcd_display_string(str(datetime.now().time()), 1)
        display.lcd_display_string(str(IP), 2)
        # Uncomment the following line to loop with 1 sec delay
        # sleep(1)
except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    display.lcd_clear()
