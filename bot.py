#!/usr/bin/python
# coding=utf-8
import config  # config file
from telegram.ext import CommandHandler
from imp import reload  # module to up other modules
from lxml import html
import requests


from telegram.ext import Updater


updater = Updater(token=config.token)
dispatcher = updater.dispatcher


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Hello! use /h to help")


def h(bot, update):
    reload(config)
    bot.sendMessage(chat_id=update.message.chat_id, text='''List of available commands: 
    /id - id user to access to download torrents
    /up - download torrent
    ''')


# Get your id to access
def myid(bot, update):
    userid = update.message.from_user.id
    bot.sendMessage(chat_id=update.message.chat_id, text=userid)


# Upload torrent
def up(bot, update, args):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin:  # if user in admin list then do
        login_url = 'https://dostup.website/http://rutracker.org/forum/login.php'
        search_url = 'https://dostup.website/http://rutracker.org/forum/tracker.php?nm=%s'
        concreteUrl = "https://dostup.website/http://rutracker.org/forum/%s"
        login_qbit_url = "http://localhost:8080/login"
        download_qbit_url = "http://localhost:8080/command/download"
        post_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '69',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': '_ym_uid=1498938755451805387; _ym_isad=2',
            'Host': 'dostup.website',
            'Origin': 'https//dostup.website',
            'Referer': 'https//dostup.website/http://rutracker.org/forum/index.php',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 '
                          'Safari/537.36',
            'X-Compress': 'null'
        }
        post_headers_qbit = {
            'Referer': 'http://localhost:8080',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        post_headers_download_qbit = {
            'Referer': 'http://localhost:8080'
        }

        data = {
            "login_username": config.login_rutracker,
            "login_password": config.pass_rutracker,
            "login": "%E2%F5%EE%E4"
        }
        data_qbit = {
            "username": config.login_qbittorrent,
            "password": config.pass_qbittorrent
        }
        session = requests.Session()
        # Login url
        session.post(login_url, data=data, headers=post_headers)

        # Get list torrents by query
        page = session.get(search_url % ' '.join(args))

        tree = html.fromstring(page.content)
        link = tree.xpath('//*[@id="tor-tbl"]/tbody/tr[1]/td[4]/div[1]/a/@href')

        # Get link to download torrent
        concrete_page = session.get(concreteUrl % link[0])
        concrete_tree = html.fromstring(concrete_page.content)
        magnet = concrete_tree.xpath("//a[@class='med magnet-link magnet-link-16']/@href")

        # Run qbittorrent to download torrent
        # Login
        session.post(login_qbit_url, data=data_qbit, headers=post_headers_qbit)

        data_download_qbit = {
            "urls": magnet[0],
            "savepath": "/home/pimshtein/Видео/",
            "category": "movies"
        }
        download_qbit_result = session.post(
            download_qbit_url,
            data=data_download_qbit,
            headers=post_headers_download_qbit
        )
        result = str(download_qbit_result) + str(data_download_qbit)
        if download_qbit_result.status_code == 200:
            result = 'Download started'
        bot.sendMessage(chat_id=update.message.chat_id, text=result)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

myid_handler = CommandHandler('id', myid)
dispatcher.add_handler(myid_handler)

help_handler = CommandHandler('h', h)
dispatcher.add_handler(help_handler)

up_handler = CommandHandler('up', up, pass_args=True)
dispatcher.add_handler(up_handler)

updater.start_polling()
