import json
import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

script_directory = os.path.dirname(os.path.abspath(__file__))
secrets_path = os.path.join(script_directory, 'SECRETS.json')
with open(secrets_path, 'r') as secrets_file:
    secrets = json.load(secrets_file)
SPOTIFY_CLIENT_ID = secrets['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = secrets['SPOTIFY_CLIENT_SECRET']
SPOTIFY_REDIRECT_URI = secrets['SPOTIFY_REDIRECT_URI']

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI,
                              scope='user-read-playback-state'))

current_track = sp.current_playback()

print(current_track)