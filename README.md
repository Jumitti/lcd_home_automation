# LCD
This repository contains all the code for interfacing with a **16x2 character I2C liquid-crystal display (LCD)**. This accompanies my **Youtube tutorial**: [Raspberry Pi - Mini LCD Display Tutorial](https://www.youtube.com/watch?v=fR5XhHYzUK0).

<p align="center">
  <a href="https://www.youtube.com/watch?v=fR5XhHYzUK0">
    <img src="imgs/thumb-yt-rpiguy-lcd-tutorial.png" width="80%">
  </a>
</p>

You can buy one of these great little I2C LCD on eBay or somewhere like [the Pi Hut](https://thepihut.com/search?type=product&q=lcd).

# Installation, implementation and contributions

Please refer to [Original repo LCD](https://github.com/the-raspberry-pi-guy/lcd)

I left the original repo in my fork for simplicity.

# Home Automation

I'm sorry for the length of the explanations. It’s a “big home automation project”. 

I separated it into 3 files to go step by step:
- ```demo_HApart1_temperature.py```
- ```demo_HApart2_now_playing.py```
- ```demo_HApart3_telegram.py```

This means that what you learn in ```demo_HApart1_temperature.py``` will be used in ```demo_HApart2_now_playing.py``` and ```demo_HApart2_now_playing.py``` in ```demo_HApart3_telegram.py```.
This project is above all a proof of concept. But by going step by step you will understand that you can modify it for your needs.

## Temperature

To get the CPU temperature it's not very complicated. Answers were given in the [Issues](https://github.com/the-raspberry-pi-guy/lcd/issues/58) of this GitHub Repo too.

On the other hand, to get the temperature of my house (especially my apartment), I used a DS18B20 thermal probe.

For the installation of the DS18B20 probe, I refer you to this [Tutorial](https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/
). I followed it for the probe part. Then for the display on the LCD I used this GitHub repo.

If you followed the steps, the temperatures save to ``w1_slave``. In the script, change the path of ``temp_file`` depending on where your ``w1_slave`` is located

<p align="center">
  <img src="imgs/demo_HApart1_temperature.jpg" width="50%">
</p>

## Now playing

For this step we will need to use the APIs.

APIs generally require a token and an ID. The "token" represents the instance that you will call to obtain the information and the ID is you. For security reasons I never write the token and ID directly in the code. You never know.

To avoid writing API information in the code, I use a ``SECRETS.json`` in the same place as the LCD script. The scripts then read the ``SECRETS.json`` to get the information.
```
{
  "TELEGRAM_ID_OWNER": YOUR_TELEGRAM_ID,
  "TELEGRAM_BOT_TOKEN": "YOUR_TELEGRAM_BOT_TOKEN",
  "SPOTIFY_CLIENT_ID": "YOUR_SPOTIFY_CLIENT_ID",
  "SPOTIFY_CLIENT_SECRET": "YOUR_SPOTIFY_CLIENT_SECRET",
  "SPOTIFY_REDIRECT_URI": "YOUR_SPOTIFY_REDIRECT_URI",
  "TRAKT_CLIENT_ID": "YOUR_TRAKT_CLIENT_ID",
  "TRAKT_USERNAME": "YOUR_TRAKT_USERNAME"
}
```
*Note: There are also already the keys for Telegram which we will see later*

### For Trakt

Trakt.tv is a smartphone application and website that allows you to follow the progress of our films and series. They have a function that allows you to directly track when an episode or film is playing. You can use Trakt.tv with Kodi, Netflix, Plex, VLC... I refer you directly to [Trakt.tv](https://trakt.tv/home)

1. Create an account on Trakt.tv
2. Replace "YOUR_TRAKT_USERNAME" with your "Username" in the ``SECRETS.json``
3. Go to ``Settings > Your API apps`` and create an API app
4. In your API app, you will find "Client ID". Replace "YOUR_TRAKT_CLIENT_ID"  with your "Client ID" in the SECRETS.json

### For Spotify

For Spotify it's a little more complicated. But we'll take it easy.

1. Create a [Spotify API](https://developer.spotify.com), configure Redirect URI (e.g http://localhost:9090), select Web API.
2. Go to the ``Settings`` of your Spotify API.
3. In the ``Basic information tab``, you will find the "Client ID", the "Client Secret" and the "Redirect URI" (which you set by configuring the API)
4. Replace the information from SECRETS.json as you did for Trakt.tv
3. Add your Spotify account in the ``User Management tab``

For this step I suggest you do it on Windows. The Spotify API needs a connection to a web page for proper authentication. Once the connection is verified, a .cache file is created. It is this file that you can drag to the root of the LCD folder.

*Note: .cache is a hidden file*


