# Torrent bot
Torrent bot can downloading torrent from rutracker.org by link and name of torrent.
If loading by url, use -u key.
If loading by name, the bot chooses first of link.

Installation on debian-like system. Use sudo:
1. Clone project:
git clone git@github.com:pimshtein/torrent_bot.git
2. Rename bot.example to bot and config.py.example to config.py
(both files are into .gitignore).
3. Create a service file:
touch /etc/systemd/system/torrent-bot.service
4. Change rights:
chmod 664 /etc/systemd/system/torrent-bot.service
5. Add to torrent-bot.service this content:  

[Unit]  
Description=Torrent bot  
After=network.target  
  
[Service]  
Type=simple  
User=user (on behalf of whom to run)  
ExecStart=path to bot.sh  
  
[Install]  
WantedBy=multi-user.target  
6. Write path to bot.py in bot.sh:
python3 /your_path/bot.py
7. Feel values in config.py
* token - your token from @FatherBot
* id - your id (send / id for the bot the first time the bot is started)