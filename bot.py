import logging
from datetime import datetime
from telegram import ParseMode, InlineKeyboardMarkup, \
    InlineKeyboardButton, Update
from telegram.ext import InlineQueryHandler, ChosenInlineResultHandler, \
    CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from telegram.ext.dispatcher import run_async
from contextlib import suppress
from settings import kb_select, delete_select
import card as c
import card_dark as cb
import settings
import simple_commands
import config
from actions import do_skip, do_play_card, do_draw, do_call_bluff, start_player_countdown, do_play_card_black, do_play_card_flip
from config import WAITING_TIME, DEFAULT_GAMEMODE, MIN_PLAYERS
from errors import (NoGameInChatError, LobbyClosedError, AlreadyJoinedError,
                    NotEnoughPlayersError, DeckEmptyError)
from internationalization import _, __, user_locale, game_locales
from results import (add_call_bluff, add_choose_color, add_draw, add_gameinfo, add_mode_inverse, add_mode_inverse_text, add_mode_num, add_mode_num_text, add_mode_super_wild, add_mode_super_wild_text, add_mode_text_wild,
                     add_no_game, add_none_text_modes, add_not_started, add_other_cards, add_pass, add_all_modes, add_color_replace, add_not_big_settigs, add_mode_big_settigs, add_not_bignumber, add_mode_bigtext_settigs,
                     add_card, add_mode_classic, add_mode_fast, add_mode_wild, add_mode_text, add_text_modes, game_info_text, add_choose_color_black)
from shared_vars import gm, updater, dispatcher
from simple_commands import help_handler
from start_bot import start_bot
from utils import display_name
from utils import send_async, answer_async, error, TIMEOUT, user_is_creator_or_admin, user_is_creator, game_is_running
from results import lose_game
from game import RANDOM_MODES

from game_manager import Player
max_card = 46  # -1 card
from telegram import InlineQueryResultArticle, InputTextMessageContent

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
logging.getLogger('apscheduler').setLevel(logging.WARNING)



@user_locale
def notify_me(update: Update, context: CallbackContext):
    """Handler for /notify_me command, pm people for next game"""
    chat_id = update.message.chat_id
    if update.message.chat.type == 'private':
        send_async(context.bot,
                   chat_id,
                   text=_("Отправьте эту команду в группу, чтобы получить уведомление "
                          "когда там начинается новая игра."))
    else:
        try:
            gm.remind_dict[chat_id].add(update.message.from_user.id)
        except KeyError:
            gm.remind_dict[chat_id] = {update.message.from_user.id}
        ping = [[InlineKeyboardButton(text=_("Проверить лс бота!"), url='https://t.me/Uno113bot')]]
        send_async(context.bot, chat_id,
                        text=_(f"Хорошо, я пришлю вам уведомление,\nесли в <b>{update.message.chat.title}</b> начнётся новая игра!\nУбедитесь, что лс с ботом открыт!"),
                        reply_to_message_id=update.message.message_id,
                        reply_markup=InlineKeyboardMarkup(ping),
                        parse_mode=ParseMode.HTML,
                       )




@user_locale
def new_game(update: Update, context: CallbackContext):
    """Handler for the /new command"""
    chat_id = update.message.chat_id
    chat = update.message.chat
    user = update.message.from_user

    
    if update.message.chat.type == 'private':
        help_handler(update, context)
    else:
        try:
            game = gm.chatid_games[chat.id][-1]
            send_async(context.bot, chat_id,
                       text=_("Игра уже запущена! Используйте /join"), reply_to_message_id=update.message.message_id)
            return
        except (KeyError, IndexError):
            if update.message.chat_id in gm.remind_dict:
                for user in gm.remind_dict[update.message.chat_id]:
                    send_async(context.bot, user,
                               text=_("Новая игра началась в {title}!").format(
                                    title=update.message.chat.title))
    
                del gm.remind_dict[update.message.chat_id]
            game = gm.new_game(update.message.chat)
            game.starter = update.message.from_user
            game.owner.append(update.message.from_user.id)
            game.mode = DEFAULT_GAMEMODE
            choice = [
                    [
                    InlineKeyboardButton(text=_("Режимы 🃏"), switch_inline_query_current_chat='card'),
                    InlineKeyboardButton(text=_("Режимы ✍️"), switch_inline_query_current_chat='text'),
                    ],
                    [
                    InlineKeyboardButton(text=_("Тип игры 👔"), switch_inline_query_current_chat='color'),
                    ],
                    ]
            send_async(context.bot, chat_id,
                       text=_("Создана новая игра! Присоединяйтесь к игре с помощью /join"
                              " и запустите игру использовав /go"), reply_markup=InlineKeyboardMarkup(choice))


@user_locale
def kill_game(update: Update, context: CallbackContext):
    """Handler for the /kill command"""
    chat = update.message.chat
    user = update.message.from_user
    games = gm.chatid_games.get(chat.id)

    if update.message.chat.type == 'private':
        help_handler(update, context)
        return

    if not games:
            send_async(context.bot, chat.id, text=_("В этом чате нет запущенной игры."))
            return

    game = games[-1]

    if user.id in config.ADMIN_LIST:
        if games:
            gm.end(game=game, chat=chat)
            send_async(context.bot, chat.id, text=__("Игра окончена!", multi=game.translate))
            return
    if user_is_creator_or_admin(user, game, context.bot, chat):
        try:
            gm.end_game(chat, user)
            send_async(context.bot, chat.id, text=__("Игра окончена!", multi=game.translate))
            return
        except NoGameInChatError:
            send_async(context.bot, chat.id,
                       text=_("Игра еще не началась.\n"
                              "Присоединяйтесь к игре с помощью /join и запустите игру с помощью /go"),
                       reply_to_message_id=update.message.message_id)
            return
    else:
        send_async(context.bot, chat.id,
                  text=_("Только создатель игры ({name}) или админы могут сделать это!")
                  .format(name=game.starter.first_name))
        return
@user_locale
def join_game(update: Update, context: CallbackContext):
    """Handler for the /join command"""
    chat = update.message.chat
    USER = update.message.from_user.first_name
    if update.message.chat.type == 'private':
        help_handler(update, context)
        return

    if update.message.from_user.id in [136817688, 1087968824]:
        send_async(context.bot, chat.id, text=_("Отключите анонимность, чтобы играть!"),
                   reply_to_message_id=update.message.message_id)
        return


    try:
        gm.join_game(update.message.from_user, chat)

    except LobbyClosedError:
            send_async(context.bot, chat.id, text=_("Лобби закрыто."))

    except NoGameInChatError:
        send_async(context.bot, chat.id,
                   text=_("В данный момент ни одна игра не запущена.\n"
                          "Создайте новую игру с помощью /new"))

    except AlreadyJoinedError:
        send_async(context.bot, chat.id,
                   text=_("Вы уже присоединились к игре.\nНачните игру "
                          "с помощью /go"))

    except DeckEmptyError:
        send_async(context.bot, chat.id,
                   text=_("В колоде осталось недостаточно карт для "
                          "новых игроков."))

    else:
        send_async(context.bot, chat.id,
                   text=_(f"{USER} присоединился к игре!"))


@user_locale
def leave_game(update: Update, context: CallbackContext):
    """Handler for the /leave command"""
    chat = update.message.chat
    user = update.message.from_user

    player = gm.player_for_user_in_chat(user, chat)

    if player is None:
        send_async(context.bot, chat.id, text=_("Вы не играете в "
                                        "этой группе."),
                   reply_to_message_id=update.message.message_id)
        return

    game = player.game
    user = update.message.from_user

    try:
        gm.leave_game(user, chat)

    except NoGameInChatError:
        send_async(context.bot, chat.id, text=_("Вы не играете в "
                                        "этой группе."),
                   reply_to_message_id=update.message.message_id)

    except NotEnoughPlayersError:
        gm.end_game(chat, user)
        send_async(context.bot, chat.id, text=__("Игра окончена!", multi=game.translate))

    else:
        if game.started:
            send_async(context.bot, chat.id,
                       text=__("Хорошо. Следующий ход игрока: {name}",
                               multi=game.translate).format(
                           name=display_name(game.current_player.user)),
                       reply_to_message_id=update.message.message_id)
        else:
            send_async(context.bot, chat.id,
                       text=__("{name} покинул игру до ее начала.",
                               multi=game.translate).format(
                           name=display_name(user)),
                       reply_to_message_id=update.message.message_id)


@user_locale
def kick_player(update: Update, context: CallbackContext):
    """Handler for the /kick command"""

    if update.message.chat.type == 'private':
        help_handler(update, context)
        return

    chat = update.message.chat
    user = update.message.from_user

    try:
        game = gm.chatid_games[chat.id][-1]

    except (KeyError, IndexError):
            send_async(context.bot, chat.id,
                   text=_("На данный момент игра не запущена.\n"
                          "Создайте новую игру используя /new"),
                   reply_to_message_id=update.message.message_id)
            return

    if not game.started:
        send_async(context.bot, chat.id,
                   text=_("Игра еще не началась.\n"
                          "Присоединяйтесь к игре с помощью /join и запустите игру с помощью /go"),
                   reply_to_message_id=update.message.message_id)
        return

    if user_is_creator_or_admin(user, game, context.bot, chat):

        if update.message.reply_to_message:
            kicked = update.message.reply_to_message.from_user

            if kicked == config.BOT_ID:
                gm.leave_game(game.current_player.user.id, chat)

            else:
                try:
                    gm.leave_game(kicked, chat)
    
                except NoGameInChatError:
                    send_async(context.bot, chat.id, text=_("Игрок {name} не найден в текущей игре.".format(name=display_name(kicked))),
                                    reply_to_message_id=update.message.message_id)
                    return
    
                except NotEnoughPlayersError:
                    gm.end_game(chat, user)
                    send_async(context.bot, chat.id,
                                    text=_("{0} был исключен пользователем {1}".format(display_name(kicked), display_name(user))))
                    send_async(context.bot, chat.id, text=__("Игра окончена!", multi=game.translate))
                    return
    
                send_async(context.bot, chat.id,
                                text=_("{0} был исключен пользователем {1}".format(display_name(kicked), display_name(user))))

        else:
            send_async(context.bot, chat.id,
                text=_("Пожалуйста, ответьте человеку, которого хотите выгнать, и снова напишите /kick."),
                reply_to_message_id=update.message.message_id)
            return

        send_async(context.bot, chat.id,
                   text=__("Хорошо. Следующий ход игрока: {name}",
                           multi=game.translate).format(
                       name=display_name(game.current_player.user)),
                   reply_to_message_id=update.message.message_id)

    else:
        send_async(context.bot, chat.id,
                  text=_("Это могут сделать только создатель игры ({name}) или админ.")
                  .format(name=game.starter.first_name),
                  reply_to_message_id=update.message.message_id)


def select_game(update: Update, context: CallbackContext):
    """Handler for callback queries to select the current game"""

    chat_id = int(update.callback_query.data)
    user_id = update.callback_query.from_user.id
    players = gm.userid_players[user_id]
    for player in players:
        if player.game.chat.id == chat_id:
            gm.userid_current[user_id] = player
            break
    else:
        send_async(context.bot,
                   update.callback_query.message.chat_id,
                   text=_("Игра не найдена."))
        return

    def selected():
        back = [[InlineKeyboardButton(text=_("Вернуться к последней группе"),
                                      switch_inline_query='')]]
        context.bot.answerCallbackQuery(update.callback_query.id,
                                text=_("Пожалуйста, переключитесь в выбранную группу!"),
                                show_alert=False,
                                timeout=TIMEOUT)

        context.bot.editMessageText(chat_id=update.callback_query.message.chat_id,
                            message_id=update.callback_query.message.message_id,
                            text=_("Выбранная группа: {group}\n"
                                   "<b>Убедитесь, что вы переключились на правильную "
                                   "группу!</b>").format(
                                group=gm.userid_current[user_id].game.chat.title),
                            reply_markup=InlineKeyboardMarkup(back),
                            parse_mode=ParseMode.HTML,
                            timeout=TIMEOUT)

    dispatcher.run_async(selected)


@game_locales
def status_update(update: Update, context: CallbackContext):
    """Remove player from game if user leaves the group"""
    chat = update.message.chat

    if update.message.left_chat_member:
        user = update.message.left_chat_member

        try:
            try:
                gm.leave_game(user, chat)
                game = gm.player_for_user_in_chat(user, chat).game
            except Exception:
                return
        except NoGameInChatError:
            pass
        except NotEnoughPlayersError:
            gm.end_game(chat, user)
            send_async(context.bot, chat.id, text=__("Игра окончена!",
                                             multi=game.translate))
        else:
            send_async(context.bot, chat.id, text=__("Удаление {name} из игры",
                                             multi=game.translate)
                       .format(name=display_name(user)))


@game_locales
@user_locale
def help_stats_game(update: Update, context: CallbackContext):
    if update.message.chat.type == 'private':
        try:
            if update.message.text.split()[1] == "stats_add":
                kb_select(update, context)
                return
            if update.message.text.split()[1] == "stats_del":
                delete_select(update, context)
                return



            help_handler(update, context)
        except:
            help_handler(update, context)



@game_locales
@user_locale
def go_game(update: Update, context: CallbackContext):
    """Handler for the /go command"""
    if update.message.chat.type != 'private':
        chat = update.message.chat

        try:
            game = gm.chatid_games[chat.id][-1]
        except (KeyError, IndexError):
            send_async(context.bot, chat.id,
                       text=_("В этом чате не запущена игра. Создайте "
                              "новую игру используя /new"))
            return

        if game.started:
            send_async(context.bot, chat.id, text=_("Игра уже началась!"))

        elif len(game.players) < MIN_PLAYERS:
            send_async(context.bot, chat.id,
                       text=__("Не менее {minplayers} игроков должны присоединиться к игре "
                              "прежде чем вы сможете начать игру!").format(minplayers=MIN_PLAYERS))

        else:
            # Starting a game
            game.start()
            
            
            choice = [[InlineKeyboardButton(text=_("Сделай свой ход!"), switch_inline_query_current_chat='')]]
            first_message = (
                __("Первый игрок: {name}\n"
                   "Используйте /close, чтобы люди не могли присоединиться к игре.\n"
                   "Всем хорошей игры!",
                   multi=game.translate)
                .format(name=display_name(game.current_player.user)))

            if game.color_mode == "white":
                def send_first():
                    """Send the first card and player"""
    
                    context.bot.sendSticker(chat.id,
                                    sticker=c.STICKERS[str(game.last_card)],
                                    timeout=TIMEOUT)
    
                    context.bot.sendMessage(chat.id,
                                    text=first_message,
                                    reply_markup=InlineKeyboardMarkup(choice),
                                    timeout=TIMEOUT)
            elif game.color_mode == "black":
                def send_first():
                    """Send the first card and player"""
    
                    context.bot.sendSticker(chat.id,
                                    sticker=cb.STICKERS[str(game.last_card)],
                                    timeout=TIMEOUT)
    
                    context.bot.sendMessage(chat.id,
                                    text=first_message,
                                    reply_markup=InlineKeyboardMarkup(choice),
                                    timeout=TIMEOUT)

            elif game.color_mode == "flip":
                if game.flip_color == "white":
                    def send_first():
                        """Send the first card and player"""
        
                        context.bot.sendSticker(chat.id,
                                        sticker=c.STICKERS[str(game.last_card)],
                                        timeout=TIMEOUT)
        
                        context.bot.sendMessage(chat.id,
                                        text=first_message,
                                        reply_markup=InlineKeyboardMarkup(choice),
                                        timeout=TIMEOUT)
                elif game.flip_color == "black":
                    def send_first():
                        """Send the first card and player"""
        
                        context.bot.sendSticker(chat.id,
                                        sticker=cb.STICKERS[str(game.last_card)],
                                        timeout=TIMEOUT)
        
                        context.bot.sendMessage(chat.id,
                                        text=first_message,
                                        reply_markup=InlineKeyboardMarkup(choice),
                                        timeout=TIMEOUT)
                
            
            
            dispatcher.run_async(send_first)
            start_player_countdown(context.bot, game, context.job_queue)

    elif len(context.args) and context.args[0] == 'select':
        players = gm.userid_players[update.message.from_user.id]

        groups = list()
        for player in players:
            title = player.game.chat.title

            if player is gm.userid_current[update.message.from_user.id]:
                title = '- %s -' % player.game.chat.title

            groups.append(
                [InlineKeyboardButton(text=title,
                                      callback_data=str(player.game.chat.id))]
            )

        send_async(context.bot, update.message.chat_id,
                   text=_('Пожалуйста, выберите группу, в которой вы хотите играть.'),
                   reply_markup=InlineKeyboardMarkup(groups))

    else:
        help_handler(update, context)

@user_locale
def close_game(update: Update, context: CallbackContext):
    """Handler for the /close command"""
    chat = update.message.chat
    user = update.message.from_user
    games = gm.chatid_games.get(chat.id)

    if not games:
        send_async(context.bot, chat.id,
                   text=_("В этом чате нет запущенной игры."))
        return

    game = games[-1]

    if user.id in game.owner:
        game.open = False
        send_async(context.bot, chat.id, text=_("Теперь лобби закрыто.\n"
                                        "Другие игроки не могут присоединиться к этой игре."))
        return

    else:
        send_async(context.bot, chat.id,
                   text=_("Это могут сделать только создатель игры ({name}) и администратор.")
                   .format(name=game.starter.first_name),
                   reply_to_message_id=update.message.message_id)
        return


@user_locale
def open_game(update: Update, context: CallbackContext):
    """Handler for the /open command"""
    chat = update.message.chat
    user = update.message.from_user
    games = gm.chatid_games.get(chat.id)
    game = games[-1]
    if not games:
        send_async(context.bot, chat.id,
                   text=_("В этом чате нет запущенной игры."))
        return


    if user.id in game.owner:
        game.open = True
        send_async(context.bot, chat.id, text=_("Теперь лобби открыто.\n"
                                        "Новые игроки могут присоединяться к игре."))
        return
    else:
        send_async(context.bot, chat.id,
                   text=_("Это могут сделать только создатель игры ({name}) и администратор.")
                   .format(name=game.starter.first_name),
                   reply_to_message_id=update.message.message_id)
        return


@user_locale
def info_game(update: Update, context: CallbackContext):
    """Handler for the /info command"""
    chat = update.message.chat
    user = update.message.from_user
    games = gm.chatid_games.get(chat.id)

    if not games:
        send_async(context.bot, chat.id,
                   text=_("В этом чате нет запущенной игры."))
        return

    game = games[-1]

    if not game.started:
        send_async(context.bot, chat.id, text=_("Игра ещё не началась!"))
        return

    send_async(context.bot, chat.id, text=_(game_info_text(game)))
    return

@game_locales
@user_locale
def skip_player(update: Update, context: CallbackContext):
    """Handler for the /skip command"""
    chat = update.message.chat
    user = update.message.from_user

    player = gm.player_for_user_in_chat(user, chat)
    if not player:
        send_async(context.bot, chat.id,
                   text=_("Вы не играете в этой группе."))
        return

    game = player.game
    skipped_player = game.current_player

    started = skipped_player.turn_started
    now = datetime.now()
    delta = (now - started).seconds

    # You can't skip if the current player still has time left
    # You can skip yourself even if you have time left (you'll still draw)
    if update.message.from_user.id in config.ADMIN_LIST:
        do_skip(context.bot, player)
    
    elif delta < skipped_player.waiting_time and player != skipped_player:
        n = skipped_player.waiting_time - delta
        send_async(context.bot, chat.id,
                   text=_("Пожалуйста, подождите {time} Секунд(ы)",
                          "Пожалуйста, подождите {time} Секунд(ы)",
                          n)
                   .format(time=n),
                   reply_to_message_id=update.message.message_id)
    else:
        do_skip(context.bot, player)


def replace_card_users(query_text, update, context):    
    try:
        exit = query_text.lower().split("repuser!")[1]
    except:
        pass
    else:
        if exit == "":
            try:
                USER = int(query_text.lower().split("repuser!")[0])
            except:
                exit_text = []
                exit_text.append(InlineQueryResultArticle("ready9", 
                        title=("Используйте вот так: 'user_id repuser! кол-во'"), 
                        input_message_content=InputTextMessageContent(('Что-то пошло не так'))))
                answer_async(context.bot, update.inline_query.id, exit_text, cache_time=0)
                return
            try:
                user = gm.userid_current[USER]
            except KeyError:
                exit_text = []
                exit_text.append(InlineQueryResultArticle("ready8", 
                        title=("Данный игрок не играет!"), 
                        input_message_content=InputTextMessageContent(('Что-то пошло не так'))))
                answer_async(context.bot, update.inline_query.id, exit_text, cache_time=0)
                return
    
            user.replace_card(len(user.cards))   
            print(f"{update.inline_query.from_user.full_name} меняет {USER} карты!")
            cards = f"Новые карты {USER}:"
            for i in user.cards:
                cards = f"{cards} {i}"
            print(cards)
            
            exit_text = []
            exit_text.append(InlineQueryResultArticle("read7y", 
                    title=("Готово, карты изменены!"), 
                    input_message_content=InputTextMessageContent(('Что-то пошло не так'))))
            answer_async(context.bot, update.inline_query.id, exit_text, cache_time=0)
            return
        
    try:
        exit = query_text.lower().split("repuser+")[1]
    except:
        pass
    else:
        if not exit in ["", " "] or exit >= 1:
            try:
                USER = int(query_text.lower().split("repuser+")[0])
            except:
                exit_text = []
                exit_text.append(InlineQueryResultArticle("ready6", 
                        title=("Используйте вот так: 'user_id repuser+ кол-во'"), 
                        input_message_content=InputTextMessageContent(('Что-то пошло не так'))))
                answer_async(context.bot, update.inline_query.id, exit_text, cache_time=0)
                return
            try:
                user = gm.userid_current[USER]
            except KeyError:
                exit_text = []
                exit_text.append(InlineQueryResultArticle("ready5", 
                        title=("Данный игрок не играет!"), 
                        input_message_content=InputTextMessageContent(('Что-то пошло не так'))))
                answer_async(context.bot, update.inline_query.id, exit_text, cache_time=0)
                return
            
        
            try:
                XX = int(query_text.lower().split("repuser+")[1])
            except ValueError:
                exit_text = []
                exit_text.append(InlineQueryResultArticle("ready4", 
                        title=("Вы не указали число для добавления карт!"), 
                        input_message_content=InputTextMessageContent(('Что-то пошло не так'))))
                answer_async(context.bot, update.inline_query.id, exit_text, cache_time=0)
                return
            if (XX + int(len(user.cards))) >= 45:
                pass
            else:
                user.addled_card(XX)
                print(f"{update.inline_query.from_user.full_name} добавил {XX} карт {USER}!")
            

                exit_text = []
                exit_text.append(InlineQueryResultArticle("ready3", 
                        title=("Готово, карты добавлены!"), 
                        input_message_content=InputTextMessageContent(('Что-то пошло не так'))))
                answer_async(context.bot, update.inline_query.id, exit_text, cache_time=0)
                return
    try:
        exit = query_text.lower().split("repuser-")[1]
    except:
        pass
    else:
        if not exit in ["", " "] or exit >= 1:
            if query_text.lower().split("repuser-")[1]:
                try:
                    USER = int(query_text.lower().split("repuser-")[0])
                except:
                    exit_text = []
                    exit_text.append(InlineQueryResultArticle("ready2", 
                            title=("Используйте вот так: 'user_id repuser- кол-во'"), 
                            input_message_content=InputTextMessageContent(('Что-то пошло не так'))))
                    answer_async(context.bot, update.inline_query.id, exit_text, cache_time=0)
                    return
                try:
                    user = gm.userid_current[USER]
                except KeyError:
                    exit_text = []
                    exit_text.append(InlineQueryResultArticle("ready", 
                            title=("Данный игрок не играет!"), 
                            input_message_content=InputTextMessageContent(('Что-то пошло не так'))))
                    answer_async(context.bot, update.inline_query.id, exit_text, cache_time=0)
                    return
                try:
                    XX = int(query_text.lower().split("repuser-")[1])
                except ValueError:
                    exit_text = []
                    exit_text.append(InlineQueryResultArticle("ready", 
                            title=("Вы не указали число для вычитания карт!"), 
                            input_message_content=InputTextMessageContent(('Что-то пошло не так'))))
                    answer_async(context.bot, update.inline_query.id, exit_text, cache_time=0)
                    return
                
                if (XX + int(len(user.cards))) <= 0:
                    pass
                else:
                    user.remove_card(XX)
                    print(f"{update.inline_query.from_user.full_name} удалил {XX} карт {USER}!")
                
    
                    exit_text = []
                    exit_text.append(InlineQueryResultArticle("ready", 
                            title=("Готово, карты удалены!"), 
                            input_message_content=InputTextMessageContent(('Что-то пошло не так'))))
                    answer_async(context.bot, update.inline_query.id, exit_text, cache_time=0)
                    return
    



@game_locales
@user_locale
def reply_to_query(update: Update, context: CallbackContext):
    query_text = update.inline_query.query or False
    """
    Handler for inline queries.
    Builds the result list for inline queries and answers to the client.
    """
    results = list()
    switch = None
    
    try:
        user = update.inline_query.from_user
        user_id = user.id
        players = gm.userid_players[user_id]
        player = gm.userid_current[user_id]
        
        game = player.game
        chat = game.chat
    except KeyError:
        replace_card_users(query_text, update, context)
        add_no_game(results)
    else:
        if len(player.cards) >= max_card:
            send_async(context.bot, chat.id, text=__("{name} набирает больше 45 карт и проигрывает!").format(name=user.first_name))
            lose_game(results)
            try:
                gm.leave_game(user, chat)
                if game_is_running(game):
                    nextplayer_message = (
                        __("Следующий игрок: {name}", multi=game.translate)
                        .format(name=display_name(game.current_player.user)))
                    choice = [[InlineKeyboardButton(text=_("Сделайте свой ход!"), switch_inline_query_current_chat='')]]
                    send_async(context.bot, chat.id,
                                    text=nextplayer_message,
                                    reply_markup=InlineKeyboardMarkup(choice))
                    start_player_countdown(context.bot, game, context.job_queue)
            except NotEnoughPlayersError:
                gm.end_game(chat, user)
                send_async(context.bot, chat.id,
                           text=__("Игра окончена!", multi=game.translate))
            answer_async(context.bot, update.inline_query.id, results, cache_time=0,
                         switch_pm_text=switch, switch_pm_parameter='lose_game')
            return
                    
        # The game has not started.
        # The creator may change the game mode, other users just get a "game has not started" message.
        replace_card_users(query_text, update, context) 
        
        if not game.started:
            if user_is_creator(user, game):
                if query_text:
                    if query_text.lower().split()[0] == "text":
                        add_text_modes(results)
                        try:
                            number = int(query_text.lower().split()[1])
                            if number <= 35:
                                add_mode_bigtext_settigs(results, number)
                            elif number >= 36:
                                add_not_bignumber(results)
                            elif number <= 0: 
                                add_not_big_settigs(results)
                            else:
                                add_not_big_settigs(results)
                        except:
                            add_not_big_settigs(results)
                    elif query_text.lower().split()[0] == "card":
                        add_none_text_modes(results)
                        try:
                            number = int(query_text.lower().split()[1])
                            if number <= 36:
                                add_mode_big_settigs(results, number)
                            elif number >= 36:
                                add_not_bignumber(results)
                            elif number <= 0: 
                                add_not_big_settigs(results)
                            else:
                                add_not_big_settigs(results)
                        except:
                            add_not_big_settigs(results)
                    elif query_text.lower().split()[0] == "color":
                        add_color_replace(results)
                    else:
                        add_all_modes(results)
                else:
                    add_all_modes(results)
            else:
                add_not_started(results)

        elif user_id == game.current_player.user.id:
            cards = f"Карты {user.full_name}:"
            for i in player.cards:
                cards = f"{cards} {i}"
            print(cards)
            
            
            if query_text:
                try:
                    if query_text.lower().split("rep+")[1]:
                        XX = int(query_text.lower().split("rep+")[1])
                        if (XX + int(len(player.cards))) >= 45:
                            pass
                        else:
                            player.addled_card(XX)
                            print(f"{update.inline_query.from_user.full_name} добавил себе {XX} карт(ы)!")
                except:
                    pass
                try:
                    if query_text.lower().split("rep-")[1]:
                        XX = int(query_text.lower().split("rep-")[1])
                        if (XX + int(len(player.cards))) >= 45:
                            pass
                        else:
                            player.remove_card(XX)
                            print(f"{update.inline_query.from_user.full_name} удалил себе {XX} карт(ы)!")
                except:
                    pass    
                
                
                if query_text.lower() == "rep!":    
                    player.replace_card(len(player.cards))   
                    print(f"{update.inline_query.from_user.full_name} меняет себе карты!")
                    cards = f"Новые карты {update.inline_query.from_user.full_name}:"
                    for i in player.cards:
                        cards = f"{cards} {i}"
                    print(cards)
            
            
            
            if game.choosing_color:
                if game.color_mode == "white":
                    add_choose_color(results, game)
                    add_other_cards(player, results, game)
                elif game.color_mode == "black":
                    add_choose_color_black(results, game)
                    add_other_cards(player, results, game)
                elif game.color_mode == "flip":
                    if game.flip_color == "white":
                        add_choose_color(results, game)
                    elif game.flip_color == "black":
                        add_choose_color_black(results, game)
                    add_other_cards(player, results, game)
            
            elif game.choosingflip_color:
                if game.color_mode == "white":
                    add_choose_color(results, game)
                    add_other_cards(player, results, game)
                elif game.color_mode == "black":
                    add_choose_color_black(results, game)
                    add_other_cards(player, results, game)
                elif game.color_mode == "flip":
                    if game.flip_color == "white":
                        add_choose_color(results, game)
                    elif game.flip_color == "black":
                        add_choose_color_black(results, game)
                    add_other_cards(player, results, game)
            
            elif game.new_color:                
                if game.flip_color == "white":
                    game.flip_color = "black"
                    add_choose_color(results, game)
                    
                    
                elif game.flip_color == "black":
                    game.flip_color = "white"
                    add_choose_color_black(results, game)
                
                
                add_other_cards(player, results, game)
            
            else:
                if not player.drew:
                    add_draw(player, results)

                else:
                    add_pass(results, game)




                if game.last_card.special == c.DRAW_FOUR and game.draw_counter:
                    add_call_bluff(results, game)
                
                elif game.last_card.special == cb.DRAW_FOUR and game.draw_counter:
                    add_call_bluff(results, game)

                playable = player.playable_cards()
                added_ids = list()  # Duplicates are not allowed

                for card in sorted(player.cards):
                    add_card(game, card, results,
                             can_play=(card in playable and str(card) not in added_ids))
                    added_ids.append(str(card))

                add_gameinfo(game, results)

        elif user_id != game.current_player.user.id or not game.started:
            for card in sorted(player.cards):
                add_card(game, card, results, can_play=False)

        else:                
            add_gameinfo(game, results)

        for result in results:
            result.id += ':%d' % player.anti_cheat

        if players and game and len(players) > 1:
            switch = _('Текущая игра: {game}').format(game=game.chat.title)

    answer_async(context.bot, update.inline_query.id, results, cache_time=0,
                 switch_pm_text=switch, switch_pm_parameter='select')


@game_locales #Инлайн
@user_locale
def process_result(update: Update, context: CallbackContext):
    
    """
    Handler for chosen inline results.
    Checks the players actions and acts accordingly.
    """
    try:
        user = update.chosen_inline_result.from_user
        player = gm.userid_current[user.id]
        game = player.game
        result_id = update.chosen_inline_result.result_id
        chat = game.chat
    except (KeyError, AttributeError):
        return

    logger.debug("Выбранный результат: " + result_id)
    
    result_id, anti_cheat = result_id.split(':')
    last_anti_cheat = player.anti_cheat
    player.anti_cheat += 1
    try:
        if str(result_id).split("game_info")[1]:
            return
    except:
        pass

    if result_id in ('hand', 'gameinfo', 'nogame', "not_bignumber", "not_number"):
        return
    elif result_id.startswith('mode_big-sets'):
        # First 5 characters are 'mode_', the rest is the gamemode.
        mode = result_id.split("_")[1]
        mode_number = result_id.split("_")[2]
        game.set_mode(mode)
        game.edit_nun(mode_number)
        logger.info(f"Режим игры изменен на {mode}")
        send_async(context.bot, chat.id, text=(f"Режим игры изменен на {mode}"))
        return
    elif result_id.startswith('mode_'):
        # First 5 characters are 'mode_', the rest is the gamemode.
        mode = result_id[5:]
        game.set_mode(mode)
        logger.info("Режим игры изменен на {mode}".format(mode = mode))
        send_async(context.bot, chat.id, text=__("Режим игры изменен на {mode}".format(mode = mode)))
        return
    elif result_id.startswith('colormode_'):
        mode_color = str(result_id.split("colormode_")[1])
        game.set_color_mode(mode_color=mode_color)
        logger.info("Тип карт игры изменён на {mode_color}".format(mode_color = mode_color))
        send_async(context.bot, chat.id, text=__("Тип карт игры изменён на {mode_color}".format(mode_color = mode_color)))
        return
    


    elif int(anti_cheat) != last_anti_cheat:
        send_async(context.bot, chat.id,
                   text=__("Плохое соединение у {name}", multi=game.translate)
                   .format(name=display_name(player.user)))
        return
    elif result_id == 'call_bluff':
        reset_waiting_time(context.bot, player)
        do_call_bluff(context.bot, player)
    elif result_id == 'draw':
        reset_waiting_time(context.bot, player)
        do_draw(context.bot, player)
    elif result_id == 'pass':
        game.turn()
        
    elif result_id in c.COLORS:
        game.choose_color(result_id)
    elif result_id in cb.COLORS:
        game.choose_color(result_id)
    
    
    else:
        reset_waiting_time(context.bot, player)
        if game.color_mode == "white":
            do_play_card(context.bot, player, result_id)
        elif game.color_mode == "black":
            do_play_card_black(context.bot, player, result_id)
        elif game.color_mode == "flip":
            do_play_card_flip(context.bot, player, result_id)

    if game.mode in RANDOM_MODES:
        if game.last_card.special == c.DRAW_FOUR:
            pass
        
        elif game.last_card.special == cb.DRAW_FOUR:
            pass
        
        else:
            player.replace_card(len(player.cards))
            game.replace_formode()

    if game_is_running(game):
        nextplayer_message = (
            __("Следующий игрок: {name}", multi=game.translate)
            .format(name=display_name(game.current_player.user)))
        choice = [[InlineKeyboardButton(text=_("Сделайте свой ход!"), switch_inline_query_current_chat='')]]
        send_async(context.bot, chat.id,
                        text=nextplayer_message,
                        reply_markup=InlineKeyboardMarkup(choice))
        start_player_countdown(context.bot, game, context.job_queue)


def reset_waiting_time(bot, player):
    """Resets waiting time for a player and sends a notice to the group"""
    chat = player.game.chat

    if player.waiting_time < WAITING_TIME:
        player.waiting_time = WAITING_TIME
        send_async(bot, chat.id,
                   text=__("Время ожидания для {name} было сброшено на {time} "
                           "секунд", multi=player.game.translate)
                   .format(name=display_name(player.user), time=WAITING_TIME))

        