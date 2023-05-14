
from telegram import ParseMode, InlineKeyboardMarkup, \
    InlineKeyboardButton, Update

from telegram import ParseMode, Update
from telegram.ext import CommandHandler, CallbackContext
from asyncio import sleep
from user_setting import UserSetting
from utils import send_async
from shared_vars import dispatcher
from internationalization import _, user_locale
from contextlib import suppress
import subprocess
import time

ADMIN = 943441135


@user_locale
def help_handler(update: Update, context: CallbackContext):
    """Handler for the /help command"""
    help_text = _(
"""<b>Следуйте этим шагам:</b>
1. Добавьте этого бота в группу
2. В группе начните новую игру с помощью /new или присоединитесь к уже существующей
запуск игры с /join
«3. После того, как присоединятся как минимум два игрока, начните игру с помощью»
/go
4. Введите <code>@uno113bot</code> в окно чата и нажмите <b>пробел</b>. 
Вы увидите свои карточки (некоторые из них выделены серым цветом), 
любые дополнительные параметры, такие как рисование и <b>?</b>, чтобы увидеть 
текущее состояние игры. <b>серые карты</b> - это те, которые вы 
<b>невозможно воспроизвести</b> в данный момент. 
Коснитесь параметра, чтобы выполнить 
выбранное действие.
Игроки могут присоединиться к игре в любое время. (Если игра окрыта)
Чтобы выйти из игры, используйте /leave. 
Если игроку требуется более 90 секунд, чтобы играть, 
Вы можете использовать /skip, чтобы пропустить этого игрока. 
Используйте /notify_me, чтобы получать личное сообщение при запуске новой игры.


<b>Статистика:</b>
/stats - Посмотреть вашу статистику игр
/delstats - Удалить вашу статистику игр

<b>Другие команды (только создатель игры):</b>
/close - Закрыть лобби
/open - Открыть лобби
/kill - Завершить игру
/kick - Выгнать игрока из игры 
(Ответом на сообщение пользователя)""")

    send_async(context.bot, update.message.chat_id, text=help_text,
               parse_mode=ParseMode.HTML, disable_web_page_preview=True)



@user_locale
def modes(update: Update, context: CallbackContext):
    """Handler for the /help command"""
    modes_explanation = _(
"""У этого бота UNO есть несколько режимов игры:
🎻В классическом режиме используется обычная колода UNO и нет автоматического пропуска.
🔢В \"<b>цифром</b>\" режиме используется колода UNO без специальных карт и нет автоматического пропуска.
🔁В \"<b>реверсивном</b>\" режиме используется обычная колода UNO, но все действия перевёнуты, нет автоматического пропуска.
🎻В классическом режиме используется обычная колода UNO и нет автоматического пропуска.
🚀В режиме \"<b>быстрый</b>\" используется обычная колода UNO, и бот автоматически пропускает игрока, если он слишком долго играет свой ход
🐉В режиме \"<b>дикая природа</b>\" используется колода с большим количеством специальных карт, меньшим разнообразием чисел и без автоматического пропуска.
🔥🐉В режиме \"<b>опасная дикая природа\"</b> используется колода состоящая только из специальных карт.
🌎В режиме <b>\"большой мир\"</b> используется обычная колода UNO, но в начале игры вам выдаётся <b>ОЧЕНЬ</b> много карт.
🌎🐉В режиме <b>\"большой дикий мир\"</b> используется колода с большим количеством специальных карт, в начале вам выдаётся БОЛЬШОЕ количество карт. Без автоматического пропуска.
🌎⚙️В режиме <b>\"настраиваемый мир\"</b> используется обычная колода UNO, но в начале игры вам выдаётся то количество карт, которое вы указали. (Максимум 35)
🪐В режиме \"<b>рандомном мир</b>\" используется обычная колода UNO, но при каждом ходе, карты игроков меняются!
(<b>Так-же каждый из этих режимов имеет свою текстовую версию ✍️</b>)


<b><i>Учитите, если вы наберёте больше 45 карт вы проиграете!</i></b>
Чтобы изменить режим игры, СОЗДАТЕЛЮ ИГРЫ необходимо ввести никнейм бота и пробел,
точно так же, как при розыгрыше карты, и должны появиться все параметры игрового режима.
<i>(Или же можете воспользоваться кнопками, которые появляются при создании новой игры)</i>
""")
    
    send_async(context.bot, update.message.chat_id, text=modes_explanation,
               parse_mode=ParseMode.HTML, disable_web_page_preview=True)

@user_locale
def source(update: Update, context: CallbackContext):
    """Handler for the /help command"""
    source_text = _('Этот бот является копией бесплатного программного обеспечения. И находится под лицензией "<b>AGPL</b>".\n'
      "<b>Оригинальный код доступен здесь:</b> \n"
      "https://github.com/jh0ker/mau_mau_bot")
    attributions = _("Атрибуции:\n"
      '"<b>Draw" значок от:</b> '
      '<a href="http://www.faithtoken.com/">Faithtoken</a>\n'
      '"<b>Pass" значок от:</b> '
      '<a href="http://delapouite.com/">Delapouite</a>\n'
      "Оригиналы доступны на: http://game-icons.net\n"
      "Иконки, отредактированные <b>ɳick</b>\n"
      "Перевод на русский, <a href='https://www.unorules.com/uno-flip-rules/'>uno flip</a> и отладка: <a href='https://t.me/This113bots'>This113bots</a>\n"
      "Отдельная благодарность : <a href='tg://user?id=1956508438'>MrKoteyka</a>")

    send_async(context.bot, update.message.chat_id, text=source_text + '\n' +
                                                 attributions,
               parse_mode=ParseMode.HTML, disable_web_page_preview=True)


@user_locale
def news(update: Update, context: CallbackContext):
    """Handler for the /news command"""
    chat = update.message.chat
    ping = [[InlineKeyboardButton(text=_("👨‍💻This113bots"), url='https://t.me/This113bots')]]
    send_async(context.bot, chat.id,      
                    text=_("Новости по ботам вы можете почитать тут 👇"),
                      reply_markup=InlineKeyboardMarkup(ping),
                      parse_mode=ParseMode.HTML)

  
@user_locale
def stats(update: Update, context: CallbackContext):
    user = update.message.from_user
    chat = update.message.chat
    us = UserSetting.get(id=user.id)
    if not us or not us.stats:
          ping = [[InlineKeyboardButton(text=_("Включить статистику!"), url='https://t.me/Uno113bot?start=stats_add')]]
          send_async(context.bot, chat.id,      
                    text=_("Пожалуйста, включите статистику в приватном чате с ботом."),
                      reply_to_message_id=update.message.message_id,
                      reply_markup=InlineKeyboardMarkup(ping),
                      parse_mode=ParseMode.HTML)

    else:
        stats_text = list()

        n = us.games_played
        stats_text.append(
            _("Игр сыграно: {number}",
              "Игр сыграно: {number}",
              n).format(number=n)
        )

        n = us.first_places
        m = round((us.first_places / us.games_played) * 100) if us.games_played else 0
        stats_text.append(
            _("Выиграно игр: {number}. ({percent}%)",
              "Выиграно игр: {number}. ({percent}%)",
              n).format(number=n, percent=m)
        )

        n = us.cards_played
        stats_text.append(
            _("Использовано карт: {number}",
              "Использовано карт: {number}",
              n).format(number=n)
        )

        send_async(context.bot, update.message.chat_id,
                   text='\n'.join(stats_text))





def register():
    dispatcher.add_handler(CommandHandler('botrestart', botrestart))
    dispatcher.add_handler(CommandHandler('help', help_handler))
    dispatcher.add_handler(CommandHandler('source', source))
    dispatcher.add_handler(CommandHandler('news', news))
    dispatcher.add_handler(CommandHandler('stats', stats))
    dispatcher.add_handler(CommandHandler('modes', modes))
