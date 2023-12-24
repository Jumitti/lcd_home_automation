#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import json
import os
import subprocess
from time import sleep
from time import strftime

import requests
import spotipy
from gpiozero import CPUTemperature
from spotipy.oauth2 import SpotifyOAuth

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


# Spotify now playing
def get_spotify_now_playing(sp):
    try:
        current_track = sp.current_playback()
        if current_track and current_track.get('is_playing', False):
            is_playing = 1
            track_name = current_track['item']['name']
            artists = ', '.join([artist['name'] for artist in current_track['item']['artists']])
            music = f"{track_name}-{artists}"
        else:
            is_playing = 0
            music = None
    except Exception as e:
        print(f"Error Spotify API: {e}")
        is_playing = 0
        music = None

    return is_playing, music


# Trakt now playing
def get_trakt_now_playing():
    # Settings for Trakt API
    url = f'https://api.trakt.tv/users/{TRAKT_USERNAME}/watching'
    headers = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': TRAKT_CLIENT_ID
    }

    # Retrieve now playing movie or show from Trakt
    try:
        activity_response = requests.get(url, headers=headers)

        # Check if the response status code is OK (200)
        if activity_response.status_code == 200:
            response = json.loads(activity_response.text)

            is_playing = 1
            if response['type'] == 'movie':
                movie_title = response['movie']['title']
                movie_year = response['movie']['year']
                trakt_playing = f"{movie_title} ({movie_year})"
            elif response['type'] == 'episode':
                show_title = response['show']['title']
                season_number = response['episode']['season']
                episode_number = response['episode']['number']
                trakt_playing = f"{show_title} S{season_number}E{episode_number}"

        else:
            is_playing = 0
            trakt_playing = None

    except Exception as e:
        print(f"Error Trakt API: {e}")
        is_playing = 0
        trakt_playing = None

    return is_playing, trakt_playing


# Display media on LCD
def display_media(media, media_type):
    if media_type == 'spotify':
        cc = '{0x02}'
    elif media_type == 'trakt':
        cc = '{0x03}'

    if len(media) > 15:  # If media is longer than LCD (16 blocs), scroll it !
        display.lcd_display_extended_string(cc + media[:15], 2)
        for i in range(len(media) - 14):
            display.lcd_display_extended_string(cc + media[i:i + 15], 2)
            sleep(0.5)
        sleep(0.5)
    else:
        display.lcd_display_extended_string(cc + '{:^15}'.format(media), 2)
        sleep(1)


# Retrieve information of connection to Spotify API, GPIO etc...
os.chdir("/home/pi/lcd/")  # To find .cache

script_directory = os.path.dirname(os.path.abspath(__file__))
secrets_path = os.path.join(script_directory, 'SECRETS.json')
with open(secrets_path, 'r') as secrets_file:
    secrets = json.load(secrets_file)

SPOTIFY_CLIENT_ID = secrets['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = secrets['SPOTIFY_CLIENT_SECRET']
SPOTIFY_REDIRECT_URI = secrets['SPOTIFY_REDIRECT_URI']
while True:
    try:
        cache_access = subprocess.check_output("ls -l .cache", shell=True, text=True)

        if not "rwsrwsrwt" in cache_access:
            print(cache_access)
            print('Error: Bad permissions for .cache')
            print('Execution: All permissions for .cache')
            os.system('sudo chmod 7777 .cache')
        else:
            print('Success: .cache has required permissions')
            break
    except subprocess.CalledProcessError as e:
        print(f'Error during execution: {e}')

TRAKT_USERNAME = secrets['TRAKT_USERNAME']
TRAKT_CLIENT_ID = secrets['TRAKT_CLIENT_ID']

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

cc.char_3_data = ["00011",  # Music 0x02
                  "00111",
                  "01101",
                  "01001",
                  "01001",
                  "01011",
                  "11011",
                  "11000"]

cc.char_4_data = ["00000",  # Movie/Show 0x03
                  "11101",
                  "10111",
                  "11111",
                  "11101",
                  "01000",
                  "10100",
                  "10010"]

cc.load_custom_characters_data()  # Load custom characters for LCD

# Connection to Spotify API
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI,
                              scope='user-read-playback-state'))

# Start LCD
display.lcd_clear()
print('Success: LCD ON')
display.lcd_display_string("  Hello  World  ", 1)

# Loop for LCD
while True:

    cpu = get_temp_cpu()
    house_temp = get_temp_ds18b20(temp_file)
    LCD_date = get_date()
    is_playing_music, music = get_spotify_now_playing(sp)
    is_playing_trakt, trakt_playing = get_trakt_now_playing()

    # Display on LCD
    display.lcd_clear()  # Avoid having residual characters
    display.lcd_display_string(LCD_date, 1)  # Line 1

    if is_playing_music == 0 and is_playing_trakt == 0:  # Line 2
        display.lcd_display_extended_string(' {0x00} ' + cpu[0:4] + '  {0x01} ' + house_temp[0:4], 2)
        sleep(1)
    elif is_playing_music == 1 and is_playing_trakt == 0:  # Display music (line 2)
        display_media(music, media_type='spotify')
        display.lcd_display_extended_string('{0x02}{0x00} ' + cpu[0:4] + '  {0x01} ' + house_temp[0:4] + " ", 2)
        sleep(1)

    elif is_playing_trakt == 1:  # Display movie/show (prior to music and on line 2)
        display_media(trakt_playing, media_type='trakt')
        display.lcd_display_extended_string('{0x03}{0x00} ' + cpu[0:4] + '  {0x01} ' + house_temp[0:4] + " ", 2)
        sleep(1)
