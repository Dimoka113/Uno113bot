#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Telegram bot to play UNO in group chats
# Copyright (c) 2016 Jannes Höke <uno@jhoeke.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import logging
from config import ADMIN_LIST, OPEN_LOBBY, DEFAULT_GAMEMODE, ENABLE_TRANSLATIONS, DEFAULT_COLORMODE, DEFAULT_FLIPCOLORMODE
from datetime import datetime

from deck import Deck
import card as c
import card_dark as cb


RANDOM_MODES = ["random-text", "random"]
LIST_CLASSIC = ["classic", "fast", "text", RANDOM_MODES[0], RANDOM_MODES[1]]
LIST_WILD = ["wild", "text-wild"]
LIST_SUPER_WILP = ['super-wild', 'super-wild-text']
LIST_NUMBER = 'number-text', 'number'
LIST_BIG = ['big-text', 'big', 'big-sets-text', 'big-sets']
LIST_WILD_BIG = ['big-wild', "big-wild-text"]

SETS_MODES = ['big-sets-text', 'big-sets']
BIGS_MODES = [LIST_BIG[0], LIST_BIG[1], LIST_WILD_BIG[0], LIST_WILD_BIG[1]]

class Game(object):
    """ This class represents a game of UNO """
    current_player = None
    reversed = False
    choosing_color = False
    started = False
    draw_counter = 0
    players_won = 0
    starter = None
    mode = DEFAULT_GAMEMODE
    color_mode = DEFAULT_COLORMODE
    job = None
    owner = ADMIN_LIST
    open = OPEN_LOBBY
    translate = ENABLE_TRANSLATIONS
    flip_color = DEFAULT_FLIPCOLORMODE
    new_color = False
    choosingflip_color = False
    nun = 0

    def __init__(self, chat):
        self.chat = chat
        self.last_card = None

        self.deck = Deck()

        self.logger = logging.getLogger(__name__)

    def edit_nun(self, nun):
        self.nun = nun

    @property
    def players(self):
        """Returns a list of all players in this game"""
        players = list()
        if not self.current_player:
            return players

        current_player = self.current_player
        itplayer = current_player.next
        players.append(current_player)
        while itplayer and itplayer is not current_player:
            players.append(itplayer)
            itplayer = itplayer.next
        return players

    def start(self):
        self.replace_formode()
        if self.color_mode == "white":
            self._first_card_()
            self.started = True
        elif self.color_mode == "black":
            self._first_card_black_()
            self.started = True
        elif self.color_mode == "flip":
            if self.flip_color == "white":
                self._first_card_()
                self.started = True
            elif self.flip_color == "black":
                self._first_card_black_()
                self.started = True

        if str(self.mode) in BIGS_MODES:
            for player in self.players:
                player.draw_first_big_hand()
        elif str(self.mode) in SETS_MODES:
            for player in self.players:
                player.draw_users_big_hand(nun=self.nun)
        else:
            for player in self.players:
                player.draw_first_hand()

    def replace_formode(self):
        if self.color_mode == "white":
            if self.mode == None or self.mode in LIST_CLASSIC:
                self.deck._fill_classic_(game_color=self.color_mode)
            elif self.mode in LIST_SUPER_WILP:
                self.deck._fill_super_wild_(game_color=self.color_mode)
            elif self.mode in LIST_NUMBER:
                self.deck._fill_number_(game_color=self.color_mode)
            elif self.mode in LIST_BIG:
                self.deck._fill_big_(game_color=self.color_mode)
            elif self.mode in LIST_WILD_BIG:
                self.deck._fill_big_wild_(game_color=self.color_mode)
            elif self.mode in LIST_WILD:
                self.deck._fill_wild_(game_color=self.color_mode)
            else:
                print(
                    f"Отсутствует режим '{self.mode}'. Он был заменён на 'classic'.")
                self.deck._fill_classic_(game_color=self.color_mode)

        elif self.color_mode == "black":
            if self.mode == None or self.mode in LIST_CLASSIC:
                self.deck._fill_classic_black(game_color=self.color_mode)
            elif self.mode in LIST_SUPER_WILP:
                self.deck._fill_super_wild_black(
                    game_color=self.color_mode)
            elif self.mode in LIST_NUMBER:
                self.deck._fill_number_black(game_color=self.color_mode)
            elif self.mode in LIST_BIG:
                self.deck._fill_big_black(game_color=self.color_mode)
            elif self.mode in LIST_WILD_BIG:
                self.deck._fill_big_wild_black(game_color=self.color_mode)
            elif self.mode in LIST_WILD:
                self.deck._fill_wild_black(game_color=self.color_mode)
            else:
                print(
                    f"Отсутствует режим '{self.mode}'. Он был заменён на 'classic'.")
                self.deck._fill_classic_black(game_color=self.color_mode)

        elif self.color_mode == "flip":
            if self.flip_color == "white":
                if self.mode == None or self.mode in LIST_CLASSIC:
                    self.deck._fill_classic_(game_color=self.color_mode)
                elif self.mode in LIST_SUPER_WILP:
                    self.deck._fill_super_wild_(game_color=self.color_mode)
                elif self.mode in LIST_NUMBER:
                    self.deck._fill_number_(game_color=self.color_mode)
                elif self.mode in LIST_BIG:
                    self.deck._fill_big_(game_color=self.color_mode)
                elif self.mode in LIST_WILD_BIG:
                    self.deck._fill_big_wild_(game_color=self.color_mode)
                elif self.mode in LIST_WILD:
                    self.deck._fill_wild_(game_color=self.color_mode)
                else:
                    print(
                        f"Отсутствует режим '{self.mode}'. Он был заменён на 'classic'.")
                    self.deck._fill_classic_(game_color=self.color_mode)

            elif self.flip_color == "black":
                if self.mode == None or self.mode in LIST_CLASSIC:
                    self.deck._fill_classic_black(game_color=self.color_mode)
                elif self.mode in LIST_SUPER_WILP:
                    self.deck._fill_super_wild_black(
                        game_color=self.color_mode)
                elif self.mode in LIST_NUMBER:
                    self.deck._fill_number_black(
                        game_color=self.color_mode)
                elif self.mode in LIST_BIG:
                    self.deck._fill_big_black(game_color=self.color_mode)
                elif self.mode in LIST_WILD_BIG:
                    self.deck._fill_big_wild_black(
                        game_color=self.color_mode)
                elif self.mode in LIST_WILD:
                    self.deck._fill_wild_black(game_color=self.color_mode)
                else:
                    print(
                        f"Отсутствует режим '{self.mode}'. Он был заменён на 'classic'.")
                    self.deck._fill_classic_black(
                        game_color=self.color_mode)

    def set_flip_color(self, mode):
        self.flip_color = mode

    def set_mode(self, mode):
        self.mode = mode

    def set_color_mode(self, mode_color):
        self.color_mode = mode_color

    def reverse(self):
        """Reverses the direction of game"""
        self.reversed = not self.reversed

    def turn(self):
        """Marks the turn as over and change the current player"""
        self.logger.debug("Следующий игрок")
        self.current_player = self.current_player.next
        self.current_player.drew = False
        self.current_player.turn_started = datetime.now()
        self.choosing_color = False
        self.choosingflip_color = False

    def _first_card_(self):
        # In case that the player did not select a game mode
        if not self.deck.cards:
            self.set_mode(DEFAULT_GAMEMODE)

        # The first card should not be a special card
        while not self.last_card or self.last_card.special:
            self.last_card = self.deck.draw()
            # If the card drawn was special, return it to the deck and loop again
            if self.last_card.special:
                self.deck.dismiss(self.last_card)

        self.play_card(self.last_card)

    def _first_card_black_(self):
        # In case that the player did not select a game mode
        if not self.deck.cards:
            self.set_mode(DEFAULT_GAMEMODE)

        # The first card should not be a special card
        while not self.last_card or self.last_card.special:
            self.last_card = self.deck.draw()
            # If the card drawn was special, return it to the deck and loop again
            if self.last_card.special:
                self.deck.dismiss(self.last_card)

        self.play_card_black(self.last_card)

    def play_card(self, card):
        """
        Plays a card and triggers its effects.
        Should be called only from Player.play or on game start to play the
        first card
        """
        self.deck.dismiss(self.last_card)
        self.last_card = card

        self.logger.info("Разыгрывается карта " + repr(card))
        if card.value == c.SKIP:
            self.turn()
        elif card.special == c.DRAW_FOUR:
            self.draw_counter += 4
            self.logger.debug("Счетчик розыгрыша увеличен на 4")
        elif card.value == c.DRAW_TWO:
            self.draw_counter += 2
            self.logger.debug("Счетчик розыгрыша увеличен на 2")
        elif card.value == c.REVERSE:
            # Special rule for two players
            if self.current_player is self.current_player.next.next:
                self.turn()
            else:
                self.reverse()
        if card.special == c.FLIP_CARD:
            self.logger.debug("Замена цвета...")
            self.new_color = True
        # Don't turn if the current player has to choose a color
        elif card.special not in (c.CHOOSE, c.DRAW_FOUR):
            self.turn()
        else:
            self.logger.debug("Выбор цвета...")
            self.choosing_color = True

    def play_card_black(self, card):
        """
        Plays a card and triggers its effects.
        Should be called only from Player.play or on game start to play the
        first card
        """
        self.deck.dismiss(self.last_card)
        self.last_card = card

        self.logger.info("Разыгрывается карта " + repr(card))
        if card.value == cb.SKIP:
            self.turn()
        elif card.special == cb.DRAW_FOUR:
            self.draw_counter += 4
            self.logger.debug("Счетчик розыгрыша увеличен на 4")
        elif card.value == cb.DRAW_TWO:
            self.draw_counter += 2
            self.logger.debug("Счетчик розыгрыша увеличен на 2")
        elif card.value == cb.REVERSE:
            # Special rule for two players
            if self.current_player is self.current_player.next.next:
                self.turn()
            else:
                self.reverse()

        if card.special == cb.FLIP_CARD:
            self.logger.debug("Замена цвета...")
            self.new_color = True

        # Don't turn if the current player has to choose a color
        if card.special not in (cb.CHOOSE, cb.DRAW_FOUR):
            self.turn()
        else:
            self.logger.debug("Выбор цвета...")
            self.choosing_color = True

    def choose_color(self, color):
        """Carries out the color choosing and turns the game"""
        self.last_card.color = color
        self.turn()
