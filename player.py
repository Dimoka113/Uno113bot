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
from datetime import datetime
import card_dark as cb
import card as c
from errors import DeckEmptyError
from config import WAITING_TIME


class Player(object):
    """
    This class represents a player.
    It is basically a doubly-linked ring list with the option to reverse the
    direction. On initialization, it will connect itself to a game and its
    other players by placing itself behind the current player.
    """

    def __init__(self, game, user):
        self.cards = list()
        self.game = game
        self.user = user
        self.logger = logging.getLogger(__name__)

        # Check if this player is the first player in this game.
        if game.current_player:
            self.next = game.current_player
            self.prev = game.current_player.prev
            game.current_player.prev.next = self
            game.current_player.prev = self
        else:
            self._next = self
            self._prev = self
            game.current_player = self

        self.bluffing = False
        self.drew = False
        self.anti_cheat = 0
        self.turn_started = datetime.now()
        self.waiting_time = WAITING_TIME

    def draw_users_big_hand(self, nun):
        number = int(nun)
        try:
            for _ in range(number):
                self.cards.append(self.game.deck.draw())
        except DeckEmptyError:
            for card in self.cards:
                self.game.deck.dismiss(card)

            raise



    def draw_first_big_hand(self):
        try:
            for _ in range(25):
                self.cards.append(self.game.deck.draw())
        except DeckEmptyError:
            for card in self.cards:
                self.game.deck.dismiss(card)

            raise

    def addled_card(self, nun: int):
        try:
            for _ in range(nun):
                self.cards.append(self.game.deck.draw())
        except DeckEmptyError:
            for card in self.cards:
                self.game.deck.dismiss(card)

            raise


    def remove_card(self, nun: int):
        try:
            for _ in range(nun):
                self.cards.pop(-1)
        except DeckEmptyError:
            for card in self.cards:
                self.game.deck.dismiss(card)

            raise


    def replace_card(self, nun: int):
        self.cards = []
        try:
            for _ in range(nun):
                self.cards.append(self.game.deck.draw())
        except DeckEmptyError:
            for card in self.cards:
                self.game.deck.dismiss(card)

            raise



    def draw_first_hand(self):
        try:
            for _ in range(7):
                self.cards.append(self.game.deck.draw())
        except DeckEmptyError:
            for card in self.cards:
                self.game.deck.dismiss(card)

            raise

    def leave(self):
        """Removes player from the game and closes the gap in the list"""
        if self.next is self:
            return

        self.next.prev = self.prev
        self.prev.next = self.next
        self.next = None
        self.prev = None

        for card in self.cards:
            self.game.deck.dismiss(card)

        self.cards = list()

    def __repr__(self):
        return repr(self.user)

    def __str__(self):
        return str(self.user)

    @property
    def next(self):
        return self._next if not self.game.reversed else self._prev

    @next.setter
    def next(self, player):
        if not self.game.reversed:
            self._next = player
        else:
            self._prev = player

    @property
    def prev(self):
        return self._prev if not self.game.reversed else self._next

    @prev.setter
    def prev(self, player):
        if not self.game.reversed:
            self._prev = player
        else:
            self._next = player

    def draw(self):
        """Draws 1+ cards from the deck, depending on the draw counter"""
        _amount = self.game.draw_counter or 1

        try:
            for _ in range(_amount):
                self.cards.append(self.game.deck.draw())

        except DeckEmptyError:
            raise

        finally:
            self.game.draw_counter = 0
            self.drew = True

    def play(self, card):
        """Plays a card and removes it from hand"""
        self.cards.remove(card)
        self.game.play_card(card)

    def playable_cards(self):
        """Returns a list of the cards this player can play right now"""

        playable = list()
        last = self.game.last_card

        self.logger.debug("Последняя карта была " + str(last))

        cards = self.cards

        # You may only play a +4 if you have no cards of the correct color
        self.bluffing = False
        for card in cards:
            if self._card_playable(card):
                self.logger.debug("Соответствие!")
                playable.append(card)

                self.bluffing = (self.bluffing or card.color == last.color)

        # You may not play a chooser or +4 as your last card
        if len(self.cards) == 1 and self.cards[0].special:
            return list()

        return playable

    def _card_playable(self, card):
        """Check a single card if it can be played"""

        is_playable = True
        last = self.game.last_card
        mode = self.game.mode in ['inverse', 'inverse-text']
        self.logger.debug("Проверка карты " + str(card))

        if self.game.color_mode == "white":
            if not mode:
                if (card.color != last.color and card.value != last.value and
                        not card.special):
                    self.logger.debug("Цвет или номинал карты не совпадают")
                    is_playable = False
                elif last.value == c.DRAW_TWO and not \
                        card.value == c.DRAW_TWO and self.game.draw_counter:
                    self.logger.debug("Игрок должен сделать ничью и не может контратаковать")
                    is_playable = False
                elif last.special == c.DRAW_FOUR and self.game.draw_counter:
                    self.logger.debug("Игрок должен сделать ничью и не может контратаковать")
                    is_playable = False
                elif (( 
                        last.special == c.CHOOSE or 
                        last.special == c.DRAW_FOUR or
                        last.special == c.FLIP_CARD
                        
                        ) and
                        (
                        card.special == c.CHOOSE or 
                        card.special == c.DRAW_FOUR or
                        card.special == c.FLIP_CARD
                        )):
                    self.logger.debug("Не могу играть в colorchooser на другом")
                    is_playable = False
                elif not last.color:
                    self.logger.debug("Последняя карта не имеет цвета")
                    is_playable = False
            else:
                if ((card.color == last.color or card.value == last.value) and
                        not card.special):
                    self.logger.debug("Цвет или номинал карты не совпадают")
                    is_playable = False
                elif last.value == c.DRAW_TWO and not \
                        card.value == c.DRAW_TWO and self.game.draw_counter:
                    self.logger.debug("Игрок должен сделать ничью и не может контратаковать")
                    is_playable = False
                elif last.special == c.DRAW_FOUR and self.game.draw_counter:
                    self.logger.debug("Игрок должен сделать ничью и не может контратаковать")
                    is_playable = False
                elif (( 
                        last.special == c.CHOOSE or 
                        last.special == c.DRAW_FOUR or
                        last.special == c.FLIP_CARD
                        
                        ) and
                        (
                        card.special == c.CHOOSE or 
                        card.special == c.DRAW_FOUR or
                        card.special == c.FLIP_CARD
                        )):
                        
                    self.logger.debug("Не могу играть в colorchooser на другом")
                    is_playable = False
                # elif not last.color:
                #     self.logger.debug("Последняя карта не имеет цвета")
                #     is_playable = False
    
            return is_playable
        elif self.game.color_mode == "black":
            if not mode:
                if (card.color != last.color and card.value != last.value and
                        not card.special):
                    self.logger.debug("Цвет или номинал карты не совпадают")
                    is_playable = False
                elif last.value == cb.DRAW_TWO and not \
                        card.value == cb.DRAW_TWO and self.game.draw_counter:
                    self.logger.debug("Игрок должен сделать ничью и не может контратаковать")
                    is_playable = False
                elif last.special == cb.DRAW_FOUR and self.game.draw_counter:
                    self.logger.debug("Игрок должен сделать ничью и не может контратаковать")
                    is_playable = False
                elif (( 
                        last.special == cb.CHOOSE or 
                        last.special == cb.DRAW_FOUR or
                        last.special == cb.FLIP_CARD
                    
                        ) and
                        (
                        card.special == cb.CHOOSE or 
                        card.special == cb.DRAW_FOUR or
                        card.special == cb.FLIP_CARD
                        )):
                    self.logger.debug("Не могу играть в colorchooser на другом")
                    is_playable = False
                elif not last.color:
                    self.logger.debug("Последняя карта не имеет цвета")
                    is_playable = False
            else:
                if ((card.color == last.color or card.value == last.value) and
                        not card.special):
                    self.logger.debug("Цвет или номинал карты не совпадают")
                    is_playable = False
                elif last.value == cb.DRAW_TWO and not \
                        card.value == cb.DRAW_TWO and self.game.draw_counter:
                    self.logger.debug("Игрок должен сделать ничью и не может контратаковать")
                    is_playable = False
                elif last.special == cb.DRAW_FOUR and self.game.draw_counter:
                    self.logger.debug("Игрок должен сделать ничью и не может контратаковать")
                    is_playable = False
                elif (( 
                        last.special == cb.CHOOSE or 
                        last.special == cb.DRAW_FOUR or
                        last.special == cb.FLIP_CARD

                        ) and
                        (
                        card.special == cb.CHOOSE or 
                        card.special == cb.DRAW_FOUR or 
                        card.special == cb.FLIP_CARD
                        )):
                    self.logger.debug("Не могу играть в colorchooser на другом")
                    is_playable = False
                # elif not last.color:
                #     self.logger.debug("Последняя карта не имеет цвета")
                #     is_playable = False
    
            return is_playable
        elif self.game.color_mode == "flip":
            if self.game.flip_color == "white":
                if not mode:
                    if (card.color != last.color and card.value != last.value and
                            not card.special):
                        self.logger.debug("Цвет или номинал карты не совпадают")
                        is_playable = False
                    elif last.value == c.DRAW_TWO and not \
                            card.value == c.DRAW_TWO and self.game.draw_counter:
                        self.logger.debug("Игрок должен сделать ничью и не может контратаковать")
                        is_playable = False
                    elif last.special == c.DRAW_FOUR and self.game.draw_counter:
                        self.logger.debug("Игрок должен сделать ничью и не может контратаковать")
                        is_playable = False
                    elif (( 
                            last.special == c.CHOOSE or 
                            last.special == c.DRAW_FOUR or
                            last.special == c.FLIP_CARD
                        
                            ) and
                            (
                            card.special == c.CHOOSE or 
                            card.special == c.DRAW_FOUR or
                            card.special == c.FLIP_CARD
                            )):
                        self.logger.debug("Не могу играть в colorchooser на другом")
                        is_playable = False
                    elif not last.color:
                        self.logger.debug("Последняя карта не имеет цвета")
                        is_playable = False
                else:
                    if ((card.color == last.color or card.value == last.value) and
                            not card.special):
                        self.logger.debug("Цвет или номинал карты не совпадают")
                        is_playable = False
                    elif last.value == c.DRAW_TWO and not \
                            card.value == c.DRAW_TWO and self.game.draw_counter:
                        self.logger.debug("Игрок должен сделать ничью и не может контратаковать")
                        is_playable = False
                    elif last.special == c.DRAW_FOUR and self.game.draw_counter:
                        self.logger.debug("Игрок должен сделать ничью и не может контратаковать")
                        is_playable = False
                    elif (( 
                            last.special == c.CHOOSE or 
                            last.special == c.DRAW_FOUR or
                            last.special == c.FLIP_CARD
    
                            ) and
                            (
                            card.special == c.CHOOSE or 
                            card.special == c.DRAW_FOUR or
                            card.special == c.FLIP_CARD
                            )):
                        self.logger.debug("Не могу играть в colorchooser на другом")
                        is_playable = False
                    # elif not last.color:
                    #     self.logger.debug("Последняя карта не имеет цвета")
                    #     is_playable = False
        
                return is_playable
            if self.game.flip_color == "black":
                if not mode:
                    if (card.color != last.color and card.value != last.value and
                            not card.special):
                        self.logger.debug("Цвет или номинал карты не совпадают")
                        is_playable = False
                    elif last.value == cb.DRAW_TWO and not \
                            card.value == cb.DRAW_TWO and self.game.draw_counter:
                        self.logger.debug("Игрок должен сделать ничью и не может контратаковать")
                        is_playable = False
                    elif last.special == cb.DRAW_FOUR and self.game.draw_counter:
                        self.logger.debug("Игрок должен сделать ничью и не может контратаковать")
                        is_playable = False
                    elif (( 
                            last.special == cb.CHOOSE or 
                            last.special == cb.DRAW_FOUR or
                            last.special == cb.FLIP_CARD
                        
                            ) and
                            (
                            card.special == cb.CHOOSE or 
                            card.special == cb.DRAW_FOUR or
                            card.special == cb.FLIP_CARD
                            )):
                        self.logger.debug("Не могу играть в colorchooser на другом")
                        is_playable = False
                    elif not last.color:
                        self.logger.debug("Последняя карта не имеет цвета")
                        is_playable = False
                else:
                    if ((card.color == last.color or card.value == last.value) and
                            not card.special):
                        self.logger.debug("Цвет или номинал карты не совпадают")
                        is_playable = False
                    elif last.value == cb.DRAW_TWO and not \
                            card.value == cb.DRAW_TWO and self.game.draw_counter:
                        self.logger.debug("Игрок должен сделать ничью и не может контратаковать")
                        is_playable = False
                    elif last.special == cb.DRAW_FOUR and self.game.draw_counter:
                        self.logger.debug("Игрок должен сделать ничью и не может контратаковать")
                        is_playable = False
                    elif (( 
                            last.special == cb.CHOOSE or 
                            last.special == cb.DRAW_FOUR or
                            last.special == cb.FLIP_CARD
    
                            ) and
                            (
                            card.special == cb.CHOOSE or 
                            card.special == cb.DRAW_FOUR or
                            card.special == cb.FLIP_CARD
                            )):
                        self.logger.debug("Не могу играть в colorchooser на другом")
                        is_playable = False
                    # elif not last.color:
                    #     self.logger.debug("Последняя карта не имеет цвета")
                    #     is_playable = False
        
                return is_playable
                    