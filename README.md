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

Please note that the SCRETS.json and .cache files (see below for more information) must be placed at the root of the LCD project (at the same level as the demo_.py)

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
2. Replace ``YOUR_TRAKT_USERNAME`` in the ``SECRETS.json`` with your ``Username``
3. Go to ``Settings > Your API apps`` and create an API app
4. In your API app, you will find ``Client ID``. Replace ``YOUR_TRAKT_CLIENT_ID`` in the ``SECRETS.json`` with your ``Client ID`` 

### For Spotify

For Spotify, it's a little more complicated. But we'll take it easy.

1. Create a [Spotify API](https://developer.spotify.com), configure ``Redirect URI`` (e.g http://localhost:9090), select ``Web API``
2. Go to the ``Settings`` of your Spotify API.
3. In the ``Basic information tab``, you will find the ``Client ID``, the ``Client Secret`` and the ``Redirect URI`` (which you set by configuring the API)
4. Replace the information from ``SECRETS.json`` as you did for Trakt.tv
5. Add your Spotify account in the ``User Management tab``

6. For this step I suggest you do it on Windows or with a graphic interface. The Spotify API needs a connection to a web page for proper authentication. Once the connection is verified, a ``.cache`` file is created (*note: ``.cache`` is a hidden file*). So, let's go on !
   - If you have follow previews steps, you have a ``SECRETS.json`` with Spotify parts filled.
   - Run:
   ```
   python3 get_cache_spotify.py
   ```
   - A hidden ``.cache`` file has just been created in the same folder

### Common

The script will read the ``SECRETS.json`` and ``.cache`` files. To avoid any permission conflict problems:
```
sudo chmod 7777 SECRETS.json
sudo chmod 7777 .cache
```

*Note: I added security which automatically gives all permissions to .cache. I realized that restarting the RPi can change the permissions of this file*

[Home Automation Now Playing Music Youtube Video](https://www.youtube.com/watch?v=TQ22pi4_cQY)
<p align="center">
  <img src="imgs/demo_HApart2_now_playing_music.gif" width="75%">
</p>

[Home Automation Now Playing Movie/Show Youtube Video](https://www.youtube.com/watch?v=ZqFxbg07gU8)
<p align="center">
  <img src="imgs/demo_HA_part2_now_playing_movie.gif" width="75%">
</p>

## Telegram

Why use Telegram? Because it's quite simple to use. You can code whatever you want in python and since the bot runs on the RPi it allows you to execute commands without opening an SSH or other connection. I'm sure there are ways to make it simpler but with this you can even control the RPi without being at home. You can automate events based on the time, the temperature of your CPU, your apartment...

1. How to get your **ID**:
   - send ```/getid``` to [myidbot](https://telegram.me/myidbot) on [Telegram](https://web.telegram.org/k/)
   - Copy/paste your ID in ```SECRETS.json``` at ``TELEGRAM_ID_OWNER`` without (') or (")
2. How to get your **TOKEN**:
   - Config a bot with [@BotFather](https://telegram.me/BotFather):
     - Create a bot with ```/newbot``` and follow instructions
     - Get API token with ```/mybots```, select your bot and get API token
     - Copy/paste your token in ```SECRETS.json``` at ``TELEGRAM_BOT_TOKEN`` between (') or (")
   - Don't forget to send ```/start``` at your Telegram bot

My script is clearly a mix of the functions I use the most. Some won't suit you and some you will miss.

### List of function

Just send ```/help``` to your Telegram bot and see all command ! 😊

*Tips*: you can set command from ```/help``` with [@BotFather](https://telegram.me/BotFather) to have a quick access
- copy message from ```/help```
- send ```/mybots``` to [@BotFather](https://telegram.me/BotFather) and select your Telegram bot
- select ```Edit Bot```
- select ```Edit Commands```
- paste message from ```/help``` without /

| Command         | Description                                            |
|-----------------|--------------------------------------------------------|
| `/temp`         | Get CPU temperature and house temperature from DS18B20 |
| `/quick_update` | To update and upgrade without autoremove and reboot    |
| `/update`       | To update, upgrade, autoremove AND REBOOT              |
| `/reboot`       | Sometimes it's good                                    |
| `/shutdown`     | As expected                                            |
| `/lcd_on`       | Turn ON backlight of LCD                               |
| `/lcd_off`      | Turn OFF backlight of LCD                              |
| `/test`         | Is my Telegram bot still working?                      |
| `/help`         | A little reminder                                      |

[Home Automation Telegram Bot Youtube Video](https://www.youtube.com/watch?v=zqm6V583k9I)
<p align="center">
  <img src="imgs/demo_HA_part3_telegram.gif" width="75%">
</p>

#### Control CPU temperature
RPi can heat, so to prevent an overheat I had a command to control a fan plugged at GPIO_PIN 17 to cooldown temperature:
- You can set critical temperature:
   ```
   GPIO_PIN_FAN = 17
   fan = OutputDevice(GPIO_PIN_FAN)
  
   def get_temp_cpu():
       cpu = CPUTemperature()
       temp = cpu.temperature
       cpu = str(temp)
   
       if temp > 65 and not fan.value:  # Warning hot temperature
           fan.on()
           bot.sendMessage(TELEGRAM_ID_OWNER, f"WARNING! Temperature too HOT! {cpu[0:4]}°C")
       elif temp > 85:  # Alert too hot temperature  + shutdown
           fan.on()
           bot.sendMessage(TELEGRAM_ID_OWNER, f"ALERT! CRITICAL TEMPERATURE! {cpu[0:4]}°C ! SHUTDOWN !")
           os.system('sudo shutdown now')
       elif temp < 55 and fan.value:  # Temperature under control
           fan.off()
           bot.sendMessage(TELEGRAM_ID_OWNER, f"Temperature under control. {cpu[0:4]}°C. Good job !")
   
       return cpu
   ```

#### Auto update
I add a function to auto-update your Raspberry every monday @ 02:30 and major update with reboot appends every 1st of each month @ 02:00.
I always plugged a LED at GPIO_PIN 27 to see when RPi do the update.

- Day: M=0; T=1; W=2...
    ```
    GPIO_PIN_UPDATE = 27
    update = OutputDevice(GPIO_PIN_UPDATE)
  
    # Quick update every monday @ 2:30
    if day == 0 and hour == '02:30':
        bot.sendMessage(TELEGRAM_ID_OWNER, 'Starting weekly update...')
        os.system('sudo apt-get update -y')
        bot.sendMessage(TELEGRAM_ID_OWNER, 'Weekly update done.\nStarting weekly upgrade...')
        os.system('sudo apt-get upgrade -y')
        bot.sendMessage(TELEGRAM_ID_OWNER, 'Weekly upgrade done')
    
    # Update every 1st of month @ 2:00
    if date == '1' and hour == '02:00':
        bot.sendMessage(TELEGRAM_ID_OWNER, 'Starting monthly update...')
        os.system('sudo apt-get update -y')
        bot.sendMessage(TELEGRAM_ID_OWNER, 'Monthly update done.\nStarting monthly upgrade...')
        os.system('sudo apt-get upgrade -y')
        bot.sendMessage(TELEGRAM_ID_OWNER, 'Monthly upgrade done.\nStarting monthly autoremove...')
        os.system('sudo apt-get autoremove -y')
        bot.sendMessage(TELEGRAM_ID_OWNER, 'Monthly autoremove done.\nStarting reboot...\nSee U soon')
    ```

## Conclusion

If you have any questions, I invite you to create Issues. I would be happy to help you. I tried to make nice documentation and a fairly quick and concise tutorial.

But I hope that with 3 little scripts, you will find what you are looking for


