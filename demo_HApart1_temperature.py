#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os
from time import sleep
from time import strftime

from gpiozero import CPUTemperature

# Import necessary libraries for communication and display use
import drivers


# Retrieve CPU temperatures
def get_temp_cpu():
    cpu = CPUTemperature()
    temp = cpu.temperature
    cpu = str(temp)

    return cpu


# Retrieve ambient temperature from DS18B20
def get_temp_ds18b20(temp_file):
    try:
        if len(temp_file) > 0:
            temperature = ds18b20(temp_file[0])
            house_temp = str(temperature)

    except Exception as e:
        print(f"Error DS18B20: {e}")
        house_temp = "n.d"

    return house_temp


# House temperature
def ds18b20(temp_file):
    temp_file = open(temp_file)
    temp = temp_file.read()
    temp_file.close()
    temp_value = temp.split("\n")[1]
    temp_output = temp_value.split(" ")[9]
    return float(temp_output[2:]) / 1000


# Retrieve date, time and gestion control
def get_date():
    LCD_date = str(strftime("%a %d.%m  %H:%M"))
    return LCD_date


temp_file = glob.glob("/sys/bus/w1/devices/28*/w1_slave")  # File location for ambient temp from DS18B204

# Load the driver and set it to "display"
# If you use something from the driver library use the "display." prefix first
display = drivers.Lcd()

# Custom character for LCD
cc = drivers.CustomCharacters(display)

cc.char_1_data = ["01010",  # CPU 0x00
                  "11111",
                  "10001",
                  "10101",
                  "10001",
                  "11111",
                  "01010",
                  "00000"]

cc.char_2_data = ["00100",  # House 0x01
                  "01110",
                  "11011",
                  "10001",
                  "10101",
                  "10101",
                  "11111",
                  "00000"]

cc.load_custom_characters_data()  # Load custom characters for LCD

# Start LCD
display.lcd_clear()
print('Success: LCD ON')
display.lcd_display_string("  Hello  World  ", 1)

# Loop for LCD
while True:

    cpu = get_temp_cpu()
    house_temp = get_temp_ds18b20(temp_file)
    LCD_date = get_date()

    # Display on LCD
    display.lcd_clear()  # Avoid having residual characters
    display.lcd_display_string(LCD_date, 1)  # Line 1
    display.lcd_display_extended_string(' {0x00} ' + cpu[0:4] + '  {0x01} ' + house_temp[0:4], 2)  # Line 2
    sleep(1)
