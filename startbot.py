from telegram.ext import (InlineQueryHandler, ChosenInlineResultHandler, 
    CommandHandler, MessageHandler, Filters, CallbackQueryHandler)
from telegram.ext.dispatcher import run_async
import settings
import simple_commands
from shared_vars import updater, dispatcher
from start_bot import start_bot
from utils import error
import bot

new = "new"                 #Начать новую игру
join = "join"               #Присоединиться к текущей игре.
go = "go"                   #"Запустить игру.
leave = "leave"             #Выйти из игры, в которой вы находитесь.
close = "close"             #Закрыть игровое лобби.
open = "open"               #Открыть игровое лобби.
kill = "kill"               #Закончить игру.
game = "game"               #Информация о текущей игре.
kick = "kick"               #Выгнать игроков из игры.
skip = "skip"               # Пропустить текущего игрока.
notify_me = "notify_me"     #Уведомление, когда в группе начнётся новая игра.
help = "help"               #Как пользоваться этим ботом?
modes = "modes"             #Объяснение режимов игры.
stats = "stats"             #Показать статистику.
delstats = "delstats"       # Удалить статистику.
source = "source"           #См. информацию об источнике.
news = "news"               #Все новости об этом боте.

LIST_COMMANDS = [
[new, "Начать новую игру."],
[join, "Присоединиться к текущей игре."],
[go, "Запустить игру."],
[leave, "Выйти из игры, в которой вы находитесь."],
[close, "Закрыть игровое лобби."],
[open, "Открыть игровое лобби."],
[kill, "Закончить игру."],
[game, "Информация о текущей игре."],
[kick, "Выгнать игроков из игры."],
[skip, "Пропустить текущего игрока."],
[notify_me, "Уведомление, когда в группе начнётся новая игра."],
[help, "Как пользоваться этим ботом?"],
[modes, "Объяснение режимов игры."],
[stats, "Показать статистику."],
[delstats, "Удалить статистику."],
[source, "См. информацию об источнике."],
[news, "Все новости об этом боте."],
]

 











# Add all handlers to the dispatcher and run the bot
dispatcher.bot.set_my_commands(LIST_COMMANDS)
dispatcher.add_handler(InlineQueryHandler(bot.reply_to_query))
dispatcher.add_handler(ChosenInlineResultHandler(bot.process_result, pass_job_queue=True))
dispatcher.add_handler(CallbackQueryHandler(bot.select_game))
dispatcher.add_handler(CommandHandler('start', bot.help_stats_game, pass_args=True, pass_job_queue=True))
dispatcher.add_handler(CommandHandler(go, bot.go_game, pass_args=True, pass_job_queue=True))
dispatcher.add_handler(CommandHandler(new, bot.new_game))
dispatcher.add_handler(CommandHandler(kill, bot.kill_game))
dispatcher.add_handler(CommandHandler(join, bot.join_game))
dispatcher.add_handler(CommandHandler(leave, bot.leave_game))
dispatcher.add_handler(CommandHandler(kick, bot.kick_player))
dispatcher.add_handler(CommandHandler(open, bot.open_game))
dispatcher.add_handler(CommandHandler(close, bot.close_game))
dispatcher.add_handler(CommandHandler(game, bot.info_game))
dispatcher.add_handler(CommandHandler(skip, bot.skip_player))
dispatcher.add_handler(CommandHandler(notify_me, bot.notify_me))
simple_commands.register()
settings.register()
dispatcher.add_handler(MessageHandler(Filters.status_update, bot.status_update))
dispatcher.add_error_handler(error)

if __name__ == '__main__':
    print ("Уно бот запущен.")

BOT = start_bot(updater)
updater.idle()