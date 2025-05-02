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
display = emulators.LcdEmulator(TITTLE_WINDOWS="Runner LCD")

# Create object with custom characters data
cc = emulators.CustomCharactersEmulator(display, 20)

# Redefine the default characters:
# Custom caracter #1. Code {0x00}. Sprite STAND
cc.char_data[f"00"] = ["00000", "00011", "00011", "00110", "00011", "00010", "00101", "00101"]
# Custom caracter #2. Code {0x01}. Sprite RUN 1
cc.char_data[f"01"] = ["00000", "00110", "00110", "01100", "10111", "00100", "01010", "10010"]
# Custom caracter #3. Code {0x02}. Sprite RUN 2
cc.char_data[f"02"] = ["00000", "00110", "00110", "01100", "00100", "01110", "01010", "10100"]

# Custom caracter #4. Code {0x03}. Sprite JUMP1
cc.char_data[f"03"] = ["00011", "00011", "01110", "11110", "11100", "01111", "01010", "10100"]
# Custom caracter #5. Code {0x04}. Sprite JUMP2
cc.char_data[f"04"] = ["00011", "00011", "11100", "01100", "00111", "00101", "01010", "00000"]
# Custom caracter #6. Code {0x05}. Sprite JUMP3
cc.char_data[f"05"] = ["00011", "00011", "00110", "00110", "00111", "01101", "01010", "10000"]

# Custom caracter #7. Code {0x06}. Sprite SLIDE1
cc.char_data[f"06"] = ["00000", "00000", "00000", "01100", "11100", "11001", "11111", "01110"]
# Custom caracter #8. Code {0x07}. Sprite SLIDE2
cc.char_data[f"07"] = ["00000", "00000", "00111", "00111", "11100", "11100", "11010", "01110"]
# Custom caracter #9. Code {0x08}. Sprite SLIDE3
cc.char_data[f"08"] = ["00000", "01100", "01100", "11000", "11000", "11100", "01010", "10010"]

# Custom caracter #10. Code {0x09}. Sprite LIFE_0HP
cc.char_data[f"09"] = ["00000", "00000", "01010", "10101", "10001", "01010", "00100", "00000"]
# Custom caracter #11. Code {0x10}. Sprite LIFE_1HP
cc.char_data[f"10"] = ["00000", "00000", "01010", "10111", "10011", "01010", "00100", "00000"]
# Custom caracter #12. Code {0x11}. Sprite LIFE_2HP
cc.char_data[f"11"] = ["00000", "00000", "01010", "10111", "10111", "01110", "00100", "00000"]
# Custom caracter #13. Code {0x12}. Sprite LIFE_3HP
cc.char_data[f"12"] = ["00000", "00000", "01010", "11111", "11111", "01110", "00100", "00000"]
# Custom caracter #14. Code {0x13}. Sprite IMMUNITY
cc.char_data[f"13"] = ["01110", "00000", "01010", "10101", "10001", "01010", "00100", "00000"]

# Load custom characters data to CG RAM:
cc.load_custom_characters_data()

start = True
paused = True
position = 2
life = 3


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
    update_display(line1="{0x00}    PAUSE.   ", position1=position)


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
        if life == 3:
            life_code = "{0x12}"
        elif life == 2:
            life_code = "{0x11}"
        elif life == 1:
            life_code = "{0x10}"
        elif life == 0:
            life_code = "{0x09}"

        if keyboard.is_pressed('space'):
            paused = not paused
            if paused:
                pause()
            else:
                display.lcd_clear()

            while keyboard.is_pressed('space'):
                time.sleep(1 / 12)

        if not paused:
            if keyboard.is_pressed('up') and position != 1:
                for i in range(3, 6):
                    time.sleep(1 / 12)

                    if i < 5:
                        line1 = f"               {life_code}"
                        line2 = f"{{0x0{i}}}"

                    elif i == 5:
                        line1 = f"{{0x0{i}}}              {life_code}"
                        line2 = None
                        position = 1

                    update_display(line1=line1, line2=line2, position1=1, position2=2)

            elif keyboard.is_pressed('down') and position != 2:
                for i in range(6, 9):
                    time.sleep(1 / 12)

                    if i < 8:
                        line1 = f"{{0x0{i}}}              {life_code}"
                        line2 = None

                    elif i == 8:
                        line1 = f"               {life_code}"
                        line2 = f"{{0x0{i}}}"
                        position = 2

                    update_display(line1=line1, line2=line2, position1=1, position2=2)

            for i in range(3):
                time.sleep(1 / 12)

                if position == 1:
                    line1 = f"{{0x0{i}}}              {life_code}"
                    line2 = None
                if position == 2:
                    line1 = f"               {life_code}"
                    line2 = f"{{0x0{i}}}"

                update_display(line1=line1, line2=line2, position1=1, position2=2)
