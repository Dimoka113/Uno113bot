import random

import logging
import card_dark as cb
import card as c
from datetime import datetime

from telegram import Message, Chat
from telegram.ext import CallbackContext
from apscheduler.jobstores.base import JobLookupError
import json
from config import TIME_REMOVAL_AFTER_SKIP, MIN_FAST_TURN_TIME
from errors import DeckEmptyError, NotEnoughPlayersError
from internationalization import __, _
from shared_vars import gm
from user_setting import UserSetting
from utils import send_async, display_name, game_is_running
from telegram import ParseMode
logger = logging.getLogger(__name__)



class Countdown(object):
    player = None
    job_queue = None

    def __init__(self, player, job_queue):
        self.player = player
        self.job_queue = job_queue

# TODO do_skip() could get executed in another thread (it can be a job), so it looks like it can't use game.translate?


def do_skip(bot, player, job_queue=None):
    game = player.game
    chat = game.chat
    skipped_player = game.current_player
    next_player = game.current_player.next
    
    if skipped_player.waiting_time > 0:
        skipped_player.anti_cheat += 1
        skipped_player.waiting_time -= TIME_REMOVAL_AFTER_SKIP
        if (skipped_player.waiting_time < 0):
            skipped_player.waiting_time = 0

        try:
            skipped_player.draw()
        except DeckEmptyError:
            pass

        n = skipped_player.waiting_time
        send_async(bot, chat.id,
                   text=__("Время ожидания игрока "
                           "было сокращено до {time} секунд.\n"
                           "Следующий ход игрока: {name}", multi=game.translate)
                   .format(time=n,
                           name=display_name(next_player.user))
                   )
        logger.info("{player} был пропущен! "
                    .format(player=display_name(player.user)))
        game.turn()
        if job_queue:
            start_player_countdown(bot, game, job_queue)

    else:
        try:
            gm.leave_game(skipped_player.user, chat)
            send_async(bot, chat.id,
                       text=__("У {name1} закончилось время"
                               "и он был удален из игры!\n"
                               "Следующий ход игрока: {name2}", multi=game.translate)
                       .format(name1=display_name(skipped_player.user),
                               name2=display_name(next_player.user)))
            logger.info("{player} был пропущен!"
                        .format(player=display_name(player.user)))
            if job_queue:
                start_player_countdown(bot, game, job_queue)

        except NotEnoughPlayersError:
            send_async(bot, chat.id,
                       text=__("У {name} закончилось время!"
                               "и был удален из игры!\n"
                               "Игра закончилась.", multi=game.translate)
                       .format(name=display_name(skipped_player.user)))

            gm.end_game(chat, skipped_player.user)


def do_play_card(bot, player, result_id):
    """Plays the selected card and sends an update to the group if needed"""
    game = player.game
    chat = game.chat
    user = player.user
    skipped_player = game.current_player

    card = c.from_str_flip(result_id)
    player.play(card)

    us = UserSetting.get(id=user.id)
    if not us:
        us = UserSetting(id=user.id)

    if us.stats:
        us.cards_played += 1

    if game.choosing_color:
        send_async(bot, chat.id, text=__(
            "Пожалуйста, выберите цвет", multi=game.translate))

    if len(player.cards) == 1:
        send_async(bot, chat.id, text="УНО!")

    if len(player.cards) == 0:
        send_async(bot, chat.id,
                   text=__("{name} выйграл!", multi=game.translate)
                   .format(name=user.first_name))

        if us.stats:
            us.games_played += 1

            if game.players_won == 0:
                us.first_places += 1

        game.players_won += 1

        try:
            gm.leave_game(user, chat)
        except NotEnoughPlayersError:
            send_async(bot, chat.id,
                       text=__("Игра окончена!", multi=game.translate))

            us2 = UserSetting.get(id=game.current_player.user.id)
            if us2 and us2.stats:
                us2.games_played += 1

            gm.end_game(chat, user)


def do_play_card_black(bot, player, result_id):
    """Plays the selected card and sends an update to the group if needed"""
    game = player.game
    chat = game.chat
    user = player.user
    skipped_player = game.current_player

    card = cb.from_str_flip(result_id)
    player.play(card)

    us = UserSetting.get(id=user.id)
    if not us:
        us = UserSetting(id=user.id)

    if us.stats:
        us.cards_played += 1

    if game.choosing_color:
        send_async(bot, chat.id, text=__(
            "Пожалуйста, выберите цвет", multi=game.translate))

    if len(player.cards) == 1:
        send_async(bot, chat.id, text="УНО!")

    if len(player.cards) == 0:
        send_async(bot, chat.id,
                   text=__("{name} выйграл!", multi=game.translate)
                   .format(name=user.first_name))

        if us.stats:
            us.games_played += 1

            if game.players_won == 0:
                us.first_places += 1

        game.players_won += 1

        try:
            gm.leave_game(user, chat)
        except NotEnoughPlayersError:
            send_async(bot, chat.id,
                       text=__("Игра окончена!", multi=game.translate))

            us2 = UserSetting.get(id=game.current_player.user.id)
            if us2 and us2.stats:
                us2.games_played += 1

            gm.end_game(chat, user)


def do_play_card_flip(bot, player, result_id):
    """Plays the selected card and sends an update to the group if needed"""
    game = player.game
    chat = game.chat
    user = player.user
    skipped_player = game.current_player

    if game.flip_color == "white":
        card = c.from_str_flip(result_id)
        player.play(card)
    elif game.flip_color == "black":
        card = cb.from_str_flip(result_id)
        player.play(card)

    us = UserSetting.get(id=user.id)
    if not us:
        us = UserSetting(id=user.id)

    if us.stats:
        us.cards_played += 1

    if game.new_color:
        if game.flip_color == "black":
            game.flip_color = "white"
        elif game.flip_color == "white":
            game.flip_color = "black"

        game.replace_formode()
        for ier in gm.userid_players:
            player1 = gm.userid_current[ier]
            player1.replace_card(len(player1.cards))

        game.new_color = False
        game.choosingflip_color = True
        send_async(
            bot, chat.id, text="<b>Происходит разворот карт!</b>\nПожалуйста, выберите новый цвет", parse_mode=ParseMode.HTML)

    if game.choosing_color:
        send_async(bot, chat.id, text=__(
            "Пожалуйста, выберите цвет", multi=game.translate))

    if len(player.cards) == 1:
        send_async(bot, chat.id, text="УНО!")

    if len(player.cards) == 0:
        send_async(bot, chat.id,
                   text=__("{name} выйграл!", multi=game.translate)
                   .format(name=user.first_name))

        if us.stats:
            us.games_played += 1

            if game.players_won == 0:
                us.first_places += 1

        game.players_won += 1

        try:
            gm.leave_game(user, chat)
        except NotEnoughPlayersError:
            send_async(bot, chat.id,
                       text=__("Игра окончена!", multi=game.translate))

            us2 = UserSetting.get(id=game.current_player.user.id)
            if us2 and us2.stats:
                us2.games_played += 1

            gm.end_game(chat, user)


def do_draw(bot, player):
    """Does the drawing"""
    game = player.game
    draw_counter_before = game.draw_counter

    try:
        player.draw()
    except DeckEmptyError:
        send_async(bot, player.game.chat.id,
                   text=__("В колоде больше нет карт.",
                           multi=game.translate))

    if game.color_mode == "white":
        if (game.last_card.value == c.DRAW_TWO or
            game.last_card.special == c.DRAW_FOUR) and \
                draw_counter_before > 0:
            game.turn()
    elif game.color_mode == "black":
        if (game.last_card.value == cb.DRAW_TWO or
            game.last_card.special == cb.DRAW_FOUR) and \
                draw_counter_before > 0:
            game.turn()
    elif game.color_mode == "flip":
        if game.flip_color == "white":
            if (game.last_card.value == c.DRAW_TWO or
                game.last_card.special == c.DRAW_FOUR) and \
                    draw_counter_before > 0:
                game.turn()
        elif game.flip_color == "black":
            if (game.last_card.value == cb.DRAW_TWO or
                game.last_card.special == cb.DRAW_FOUR) and \
                    draw_counter_before > 0:
                game.turn()


def do_call_bluff(bot, player):
    """Handles the bluff calling"""
    game = player.game
    chat = game.chat

    if player.prev.bluffing:
        send_async(bot, chat.id,
                   text=__("Да. Это блеф! {name} берёт 4 карты",
                           multi=game.translate)
                   .format(name=player.prev.user.first_name))

        try:
            player.prev.draw()
        except DeckEmptyError:
            send_async(bot, player.game.chat.id,
                       text=__("В колоде больше нет карт.",
                               multi=game.translate))

    else:
        game.draw_counter += 2
        send_async(bot, chat.id,
                   text=__("{name1} не блефовал(а)! {name2} берёт 6 карт.",
                           multi=game.translate)
                   .format(name1=player.prev.user.first_name,
                           name2=player.user.first_name))
        try:
            player.draw()
        except DeckEmptyError:
            send_async(bot, player.game.chat.id,
                       text=__("В колоде больше нет карт.",
                               multi=game.translate))

    game.turn()


def start_player_countdown(bot, game, job_queue):
    player = game.current_player
    time = player.waiting_time

    if time < MIN_FAST_TURN_TIME:
        time = MIN_FAST_TURN_TIME

    if game.mode == 'fast':
        if game.job:
            try:
                game.job.schedule_removal()
            except JobLookupError:
                pass

        job = job_queue.run_once(
            # lambda x,y: do_skip(bot, player),
            skip_job,
            time,
            context=Countdown(player, job_queue)
        )

        logger.info("Время для хода {player} уменьшилось до {время} секунд."
                    .format(player=display_name(player.user), time=time))
        player.game.job = job


def skip_job(context: CallbackContext):
    player = context.job.context.player
    game = player.game
    if game_is_running(game):
        job_queue = context.job.context.job_queue
        do_skip(context.bot, player, job_queue)
