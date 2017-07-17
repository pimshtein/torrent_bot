# Torrent bot
Install on debian-like system. Use sudo.
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

