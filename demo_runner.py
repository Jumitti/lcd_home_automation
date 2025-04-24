#! /usr/bin/env python
import time

# Just a 16x2 LCD screen simulator using Tkinter, allowing for easy testing and
# visualization of LCD displays without physical hardware. This simulator helps
# in developing and debugging LCD-based projects directly from a computer.

# Import necessary libraries for communication and display use
import emulators
from time import sleep
from datetime import datetime
import keyboard


# Load the driver and set it to "display"
# If you use something from the driver library use the "display." prefix first
display = emulators.LcdEmulator()

# Create object with custom characters data
cc = emulators.CustomCharactersEmulator(display)

# Redefine the default characters:
# Custom caracter #1. Code {0x00}. Sprite STAND
cc.char_1_data = ["00000", "00011", "00011", "00110", "00011", "00010", "00101", "00101"]
# Custom caracter #2. Code {0x01}. Sprite RUN 1
cc.char_2_data = ["00000", "00110", "00110", "01100", "10111", "00100", "01010", "10010"]
# Custom caracter #3. Code {0x02}. Sprite RUN 2
cc.char_3_data = ["00000", "00110", "00110", "01100", "00100", "01110", "01010", "10100"]

# Custom caracter #4. Code {0x03}. Sprite JUMP1
cc.char_4_data = ["00011", "00011", "01110", "11110", "11100", "01111", "01010", "10100"]
# Custom caracter #5. Code {0x04}. Sprite JUMP2
cc.char_5_data = ["00011", "00011", "11100", "01100", "00111", "00101", "01010", "00000"]
# Custom caracter #6. Code {0x05}. Sprite JUMP3
cc.char_6_data = ["00011", "00011", "00110", "00110", "00111", "01101", "01010", "10000"]

# Custom caracter #7. Code {0x06}. Sprite SLIDE1
cc.char_7_data = ["00000", "00000", "00000", "01100", "11100", "11001", "11111", "01110"]
# Custom caracter #8. Code {0x07}. Sprite SLIDE2
cc.char_8_data = ["00000", "00000", "00111", "00111", "11100", "11100", "11010", "01110"]
# Custom caracter #9. Code {0x08}. Sprite SLIDE3
cc.char_9_data = ["00000", "01100", "01100", "11000", "11000", "11100", "01010", "10010"]

# Load custom characters data to CG RAM:
cc.load_custom_characters_data()

start = True
paused = True
position = 2


def update_display(line1=None, line2=None, position1=None, position2=None):
    display.lcd_clear()
    if line1 and position1:
        display.lcd_display_extended_string(line1, position1)
    if line2 and position2:
        display.lcd_display_extended_string(line2, position2)


def run():
    for i in range(3):
        if paused:
            return

        display.lcd_display_extended_string(f"{{0x0{i}}}", line=position)
        display.lcd_clear()
        time.sleep(1 / 12)


def pause():
    display.lcd_clear()
    display.lcd_display_extended_string("{0x00} PAUSE", line=position)


while True:
    if start:
        rules = "        Use UP, DOWN and SPACE (PAUSE) to avoid obstacles        "
        j = 0
        k = 1
        l = 2
        for i in range(len(rules) - 15):

            if keyboard.is_pressed('space'):
                start = not start
                display.lcd_clear()
                break

            line1 = f"{{0x0{j}}}{{0x0{k}}}{{0x0{l}}}Runner LCD{{0x0{l}}}{{0x0{k}}}{{0x0{j}}}}}"
            j = (j + 1) % 9
            k = (k + 1) % 9
            l = (l + 1) % 9
            line2 = rules[i:i + 16]
            time.sleep(0.20)
            update_display(line1, line2, 1, 2)

    elif not start:
        if keyboard.is_pressed('space'):
            paused = not paused
            if paused:
                pause()
            else:
                display.lcd_clear()

            while keyboard.is_pressed('space'):
                time.sleep(1 / 12)

        if keyboard.is_pressed('up') and position != 1:
            for i in range(3, 6):
                time.sleep(1 / 12)

                if paused:
                    line1 = f"{{0x0{i}}} PAUSE"
                    update_display(line1=line1, position1=position)
                    break

                line1 = f"{{0x0{i}}}"

                if i == 5:
                    position = 1

                update_display(line1=line1, position1=position)

        elif keyboard.is_pressed('down') and position != 2:
            for i in range(6, 9):
                time.sleep(1 / 12)

                if paused:
                    line1 = f"{{0x0{i}}} PAUSE"
                    update_display(line1=line1, position1=position)
                    break

                line1 = f"{{0x0{i}}}"

                if i == 8:
                    position = 2

                update_display(line1=line1, position1=position)

        for i in range(3):
            time.sleep(1 / 12)

            if paused:
                line1 = f"{{0x0{i}}} PAUSE"
                update_display(line1=line1, position1=position)
                break

            line1 = f"{{0x0{i}}}"

            update_display(line1=line1, position1=position)
