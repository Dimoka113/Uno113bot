# УНО Бот

[![Лицензия: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](./ЛИЦЕНЗИЯ)

Telegram Bot, который позволяет вам играть в популярную карточную игру UNO с помощью встроенных запросов. В настоящее время бот работает как [@uno113bot](http://telegram.me/uno113bot).

Чтобы запустить бота самостоятельно, вам потребуется:
- Python (проверено с 3.4+)
- Модуль [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [Пони ORM](https://ponyorm.com/)

## Настроить:
- Получите токен бота от [@BotFather] (http://telegram.me/BotFather) и измените конфигурации в `bots/uno.json` изменив `token` и `bot_id`.
- Используйте `/setinline` и `/setinlinefeedback` с BotFather для вашего бота.
- Требования к установке (рекомендуется использование `virtualenv`): `pip install -r requirements.txt`

Вы можете изменить некоторые параметры игрового процесса, такие как время хода, минимальное количество игроков и игровой режим по умолчанию, в `bots/uno.json`.

Затем запустите бота с помощью `python3 bot.py`.

Документация по коду минимальна, но есть.