#! /usr/bin/env python

# Simple clock program. Writes the exact time.
# Demo program for the I2C 16x2 Display from Ryanteck.uk
# Created by Matthew Timmons-Brown for The Raspberry Pi Guy YouTube channel

# Import necessary libraries for communication and display use
from lcd_16x2 import drivers
from time import sleep
from datetime import datetime

import sys

if sys.platform != "linux":
    print("Warning: This script uses 'smbus', which is specific to Raspberry Pi.")
    print("You are on a different system (Windows, macOS, etc.). The demo will not function as expected.")
    print("Please try running this script on a Raspberry Pi for full functionality or use demo_emulator.py instead.")
    sys.exit(1)

# Load the driver and set it to "display"
# If you use something from the driver library use the "display." prefix first
display = drivers.Lcd()

try:
    print("Writing to display")
    display.lcd_display_string("No time to waste", 1)  # Write line of text to first line of display
    while True:
        # Write just the time to the display
        display.lcd_display_string(str(datetime.now().time()), 2)
        # Uncomment the following line to loop with 1 sec delay
        # sleep(1)
except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    display.lcd_clear()
