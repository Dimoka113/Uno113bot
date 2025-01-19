# UNO Bot

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](./LICENSE)

Telegram Bot that allows you to play the popular card game UNO via inline queries. The bot currently runs as [@unobot](http://telegram.me/unobot).

To run the bot yourself, you will need: 
- Python (tested with 3.4+)
- The [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) module
- [Pony ORM](https://ponyorm.com/)

## Setup
- Get a bot token from [@BotFather](http://telegram.me/BotFather) and change configurations in `bots/uno.json`.
- Use `/setinline` and `/setinlinefeedback` with BotFather for your bot.
- Use `/setcommands` and submit the list of commands in commandlist.txt
- Install requirements (using a `virtualenv` is recommended): `pip install -r requirements.txt`

You can change some gameplay parameters like turn times, minimum amount of players and default gamemode in `bots/uno.json`.
To find out the available modes, you can use: `/modes` command.

Then run the bot with `python3 startbot.py`.

Code documentation is minimal but there.
